#!/usr/bin/python

import urllib3, sys, json, argparse
from pprint import pprint

http = urllib3.PoolManager()

ver = "0.15"

# To find the your teamwork site name and your API key
# check the following page
# https://developer.teamwork.com/projects/finding-your-url-and-api-key/api-key-and-url
company = "YOUR_TEAMWORK_SITE_NAME"
key = "YOUR_API_KEY"

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def introText():
	print 'tw.py v' + ver + ' - Created by George Sokianos'


def getProjectIdByName(rawdata, projectName):
    projectIdFound = 0

    for pkey, projects in enumerate(rawdata["projects"]):
        if projects['name'] == projectName:
            projectIdFound = projects['id']

    return projectIdFound


def apiGetProjects():
    url = "https://{0}.teamwork.com/{1}".format(company, 'projects.json')
    headers = urllib3.util.make_headers(basic_auth=key + ":xxx")
    request = http.request('GET', url, headers=headers)

    response = request.status
    retData = json.loads(request.data)
    return retData


def apiGetTasks(pid):
    url = "https://{0}.teamwork.com/projects/{1}/tasks.json".format(company, pid)
    headers = urllib3.util.make_headers(basic_auth=key + ":xxx")
    request = http.request('GET', url, headers=headers)

    response = request.status
    retData = json.loads(request.data)
    return retData


def apiGetTaskInfo(tid):
    url = "https://{0}.teamwork.com/tasks/{1}.json".format(company, tid)
    headers = urllib3.util.make_headers(basic_auth=key + ":xxx")
    request = http.request('GET', url, headers=headers)

    response = request.status
    retData = json.loads(request.data)

    return retData


def printProjects(rawdata):
    outputMessage = ""
    projectIdFound = 0
    outputMessage += "Found " + str(len(rawdata["projects"])) + " Projects\n"

    for pkey, projects in enumerate(rawdata["projects"]):
        outputMessage += projects['id'] + '\t'
        outputMessage += projects['created-on'] + '\t'
        outputMessage += projects['name'] + '\t\t\t'
        outputMessage += "\n"

    print outputMessage


def printTaskList(rawdata):
    outputMessage = ""
    outputMessage += "Found " + str(len(rawdata["todo-items"])) + " Tasks\n"

    for tkey, tasks in enumerate(rawdata["todo-items"]):
        outputMessage += str(tasks['id']) + '\t'
        outputMessage += tasks['created-on'] + '\t'
        if 'responsible-party-names' not in tasks:
            outputMessage += ' - \t\t\t'
        else :
            outputMessage += tasks['responsible-party-names'] + '\t\t'

        outputMessage += tasks['content'] + '\t\t'
        outputMessage += '\n'

    print outputMessage


def printTaskInfo(rawdata):
    taskData = rawdata['todo-item']
    outputMessage = "\n"
    outputMessage += color.BOLD + taskData['content'] + color.END + '\n'
    outputMessage += taskData['description'] + '\n\n'

    outputMessage += taskData['project-name'] + ' > ' + taskData['todo-list-name'] + '\n'
    outputMessage += 'Status: \t' + taskData['status'] + '\n'
    outputMessage += 'Assigned: \t' + taskData['responsible-party-names'] + '\n'
    outputMessage += 'Created: \t' + taskData['created-on'] + '\n'

    nufSubtasks = len(taskData["predecessors"])
    if nufSubtasks > 0 :
        outputMessage += '\nSubtasks:\n--------\n'
        for subkey, subtasks in enumerate(taskData["predecessors"]):
            outputMessage += str(subtasks['id']) + '\t'
            outputMessage += subtasks['name']
            outputMessage += '\n'

    print outputMessage


def main(argv):
    projectName = ''
    taskId = 0
    action = ''

    # Parse the arguments
    argParser = argparse.ArgumentParser(description='This is a python script that can be used to get information from Teamwork Projects Management. You can find more info at https://github.com/walkero-gr/tw')
    argParser.add_argument('-p', '--project', action='store', dest='project_name', help='set the project name')
    argParser.add_argument('-t', '--task', action='store', dest='task_id', type=int, help='set the task ID')

    argParser.add_argument('-lt', '--list-tasks', action='store_true', default=False, dest='list_tasks', help='list tasks of the project. The project name parameter is mandatory.')
    argParser.add_argument('-lp', '--list-projects', action='store_true', default=False, dest='list_proj', help='list the available projects you have access to.')
    argParser.add_argument('-ti', '--task-info', action='store_true', default=False, dest='task_info', help='show information about the specified task. The task ID parameter is mandatory.')

    argParser.add_argument('--version', action='version', version='%(prog)s v' + ver)

    args = argParser.parse_args()

    if args.project_name :
        projectName = args.project_name
    if args.task_id :
        taskId = args.task_id
    if args.list_tasks :
        action = 'list-tasks'
    if args.list_proj :
        action = 'list-projects'
    if args.task_info :
        action = 'task-info'


    introText()

    # Check if the user edited the YOUR_TEAMWORK_SITE_NAME and YOUR_API_KEY with his own
    if company == "YOUR_TEAMWORK_SITE_NAME" or key == "YOUR_API_KEY" :
        print "You have to give to give your teamwork site name and your API key for this script to work. Please, consult the README.md file."
        sys.exit()


    if action == 'list-tasks':
        if projectName != '' :
            projectsData = apiGetProjects()
            projectId = getProjectIdByName(projectsData, projectName)

            if projectId > 0:
                print "Project ID " + projectId
                taskList = apiGetTasks(projectId)
                printTaskList(taskList)
            else:
                print "Requested project not found."
        else :
            print "You have to give a project name. Type -h to see the help text."
            sys.exit(2)

    elif action == 'list-projects':
        projectsData = apiGetProjects()
        printProjects(projectsData)
        sys.exit(2)

    elif action == 'task-info':
        try :
            int(taskId)

            if taskId > 0 :
                taskData = apiGetTaskInfo(taskId)

                if 'error' not in taskData:
                    printTaskInfo(taskData)
                elif taskData['status'] == 'error' and taskData['error'] == 'Not found':
                    print "The task you provided was not found."
                    sys.exit(2)

        except ValueError:
            if taskId == '' :
                print "You have to give a task ID. Type -h to see the help text."
            else:
                print "There was a problem with the provided task. Please check if the ID is the right one."
            sys.exit()




if __name__ == "__main__":
	main(sys.argv[1:])

