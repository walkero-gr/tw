#!/usr/bin/python

import urllib3, sys, getopt, json, subprocess
from pprint import pprint

http = urllib3.PoolManager()

ver = "0.1"

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
	print "tw v" + ver
	print "Created by George Sokianos"

def helpText():
    introText()
    print "https://github.com/walkero-gr/tw"
    print "This is a python script that can be used to get information from Teamwork Projects Management\n"
    print "tw.py [-h,-l,-s,-i] -p <projectName> -t <taskID>\n"
    print "-h\tReturns this help text\n"
    print "Parameters\n----------"
    print "-p|--project\t\tThe project name"
    print "-t|--task-id\t\tThe task ID"
    print "\nActions\n-------"
    print "The latest action overrides the previous defined, f.ex. if you give -l -s then only -s will be executed.\n"
    print "-l|--list-tasks\t\tList tasks of the project. The project name parameter is mandatory."
    print "-s|--list-projects\tList the available projects you have access to."
    print "-i|--task-info\t\tShow information about the specified task. The task ID parameter is mandatory."
    # print "-n|--new-task\t\tCreate a new task under the given project."



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


def getGitBranch():
    process = subprocess.Popen(["git", "branch"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def main(argv):


    projectName = ''
    taskId = 0
    action = ''

    try:
        opts, args = getopt.getopt(argv,"hp:t:ltnsi",["project=","task-id=","list-tasks","new-task","--list-projects","task-info"])

    except getopt.GetoptError:
        helpText()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            helpText()
            sys.exit()
        elif opt in ("-p", "--project"):
            projectName = arg.strip()
        elif opt in ("-t", "--task-id"):
            taskId = arg.strip()
        elif opt in ("-l", "--list-tasks"):
            action = 'list-tasks'
        elif opt in ("-s", "--list-projects"):
            action = 'list-projects'
        elif opt in ("-i", "--task-info"):
            action = 'task-info'

        # elif opt in ("-n", "--new-task"):
        #     action = 'new-task'


    # if len(sys.argv) < 2:
    #     helpText()
    #     sys.exit()

    introText()

    getGitBranch()

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
                print taskData

                # if taskData['status'] == 'OK':
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

