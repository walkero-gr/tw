#!/usr/bin/python

import urllib3, sys, argparse, json, subprocess, textwrap
from pprint import pprint

http = urllib3.PoolManager()

ver = "0.18"

# To find the your teamwork site name and your API key
# check the following page
# https://developer.teamwork.com/projects/finding-your-url-and-api-key/api-key-and-url
company = "YOUR_TEAMWORK_SITE_NAME"
key = "YOUR_API_KEY"

# If you always use a default branch prefix, you can add it below
# and use that when you use the --git-branch parameter
default_branch_prefix = 'TW-#'


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


def apiGetProjectTasks(pid):
    url = "https://{0}.teamwork.com/projects/{1}/tasks.json".format(company, pid)
    headers = urllib3.util.make_headers(basic_auth=key + ":xxx")
    request = http.request('GET', url, headers=headers)

    response = request.status
    retData = json.loads(request.data)
    return retData


def apiGetUserTasks(uid):
    url = "https://{0}.teamwork.com/tasks.json?responsible-party-ids={1}".format(company, uid)
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


def apiGetCurrentUser():
    url = "https://{0}.teamwork.com/{1}".format(company, 'me.json')
    headers = urllib3.util.make_headers(basic_auth=key + ":xxx")
    request = http.request('GET', url, headers=headers)

    response = request.status
    retData = json.loads(request.data)

    return retData


def printProjects(rawdata):
    print "Found " + str(len(rawdata["projects"])) + " Projects"

    for pkey, projects in enumerate(rawdata["projects"]):
        print "{0:<10} {1:<22} {2}".format(projects['id'], projects['created-on'], projects['name'])


def printTaskList(rawdata):
    strUserMaxWidth = 25

    print "Found " + str(len(rawdata["todo-items"])) + " Tasks"
    for tkey, tasks in enumerate(rawdata["todo-items"]):
        strUserLines = 0

        if 'responsible-party-names' not in tasks:
            responsibleUsers = ' - '
        else :
            responsibleUsers = textwrap.wrap(tasks['responsible-party-names'], strUserMaxWidth)
            strUserLines = len(tasks['responsible-party-names']) / strUserMaxWidth

        print "{0:<10d} {1:<22} {2:<{userWidth}} {3:20} {4}".format(tasks['id'], tasks['created-on'], responsibleUsers[0], tasks['project-name'], tasks['content'], userWidth=strUserMaxWidth+2)
        # If the string with user names is longer than the strUserMaxWidth, then print the rest of the lines under.
        # This is a pseudo wrapping way to print it
        if strUserLines > 0 :
            for idx, userLine in enumerate(responsibleUsers) :
                if idx > 0 :
                    print "{0:34}{1:<27}".format("", userLine)


def printTaskInfo(rawdata):
    taskData = rawdata['todo-item']
    outputMessage = "\n"
    outputMessage += color.BOLD + taskData['content'] + color.END + '\n'
    outputMessage += taskData['description'] + '\n\n'

    outputMessage += taskData['project-name'] + ' > ' + taskData['todo-list-name'] + '\n'
    outputMessage += 'Task ID: \t' + str(taskData['id']) + '\n'
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
    currentBranch = ''
    try :
        process = subprocess.Popen(["git", "branch"], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        outlist = output.split('\n')
        for branch in outlist:
            if '* ' in branch :
                currentBranch = branch.replace('* ', '')
    except subprocess.CalledProcessError as e:
        print e.output

    return currentBranch




def main(argv):
    taskId = 0
    projectName = ''
    action = ''
    branchPrefix = ''
    if default_branch_prefix != '' :
        branchPrefix = default_branch_prefix

    # Parse the arguments
    argParser = argparse.ArgumentParser(description='This is a python script that can be used to get information from Teamwork Projects Management. You can find more info at https://github.com/walkero-gr/tw')
    argParser.add_argument('-p', '--project', action='store', dest='project_name', help='set the project name')
    argParser.add_argument('-t', '--task', action='store', dest='task_id', type=int, help='set the task ID')
    argParser.add_argument('-bp', '--branch-prefix', action='store', dest='branch_prefix', help='set branch prefix, if any. Used with --git-branch.')

    argParser.add_argument('-lt', '--list-tasks', action='store_true', default=False, dest='list_tasks', help='list tasks of the project. The project name parameter is mandatory.')
    argParser.add_argument('-mt', '--my-tasks', action='store_true', default=False, dest='my_tasks', help='list my tasks across all project.')
    argParser.add_argument('-lp', '--list-projects', action='store_true', default=False, dest='list_proj', help='list the available projects you have access to.')
    argParser.add_argument('-ti', '--task-info', action='store_true', default=False, dest='task_info', help='show information about the specified task. The task ID parameter is mandatory.')
    argParser.add_argument('-gb', '--git-branch', action='store_true', default=False, dest='git_branch', help='show information about the task ID taken from the current GIT branch name. If task ID parameter is set, this action will be ignored.')

    argParser.add_argument('--version', action='version', version='%(prog)s v' + ver)

    args = argParser.parse_args()

    if args.project_name :
        projectName = args.project_name
    if args.task_id :
        taskId = args.task_id
    if args.branch_prefix :
        branchPrefix = args.branch_prefix
    if args.list_tasks :
        action = 'list-tasks'
    if args.list_proj :
        action = 'list-projects'
    if args.task_info :
        action = 'task-info'
    if args.my_tasks :
        action = 'my-tasks'

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
                taskList = apiGetProjectTasks(projectId)
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

    elif action == 'my-tasks':
        userData = apiGetCurrentUser()
        currentUserID = userData['person']['id']
        tasksData = apiGetUserTasks(currentUserID)
        printTaskList(tasksData)
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
            else:
                if args.git_branch :
                    gitBranch = getGitBranch()

                    if gitBranch != '' :
                        if branchPrefix != '' :
                            taskId = gitBranch.replace(branchPrefix, '')
                        else :
                            taskId = gitBranch

                        taskData = apiGetTaskInfo(taskId)

                        if 'error' not in taskData and 'Bad request' not in taskData:
                            printTaskInfo(taskData)
                        elif taskData['status'] == 'error' and taskData['error'] == 'Not found':
                            print "The task you provided was not found."
                            sys.exit(2)
                else :
                    print "You have to give a task ID. Type -h to see the help text."

        except ValueError:
            if taskId == '' :
                print "You have to give a task ID. Type -h to see the help text."
            else:
                print "There was a problem with the provided task. Please check if the ID is the right one."
            sys.exit()



if __name__ == "__main__":
	main(sys.argv[1:])

