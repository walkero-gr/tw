#!/usr/bin/python

import urllib3, sys, getopt, json
from pprint import pprint

http = urllib3.PoolManager()

ver = "0.1"

# To find the your teamwork site name and your API key
# check the following page
# https://developer.teamwork.com/projects/finding-your-url-and-api-key/api-key-and-url
company = "YOUR_TEAMWORK_SITE_NAME"
key = "YOUR_API_KEY"


def introText():
	print "\ntw v" + ver
	print "Created by George Sokianos"

def helpText():
    introText()
    print "https://github.com/walkero-gr/tw"
    print "This is a python script that can be used to get information from Teamwork Projects Management\n"
    print "tw.py [-h,-l,-s] -p <projectName>\n"
    print "Parameters\n----------"
    print "-p|--project\t\tThe project name"
    print "\nActions\n-------"
    print "The latest action overrides the previous defined, f.ex. if you give -l -s then only -s will be executed.\n"
    print "-h\t\t\tReturns this help text"
    print "-l|--list-tasks\t\tList tasks of the project. Needs given project."
    print "-s|--list-projects\tList the available projects you have access to."
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


def main(argv):
    projectName = ''
    action = ''

    try:
        opts, args = getopt.getopt(argv,"hp:ltns",["project=","list-tasks","new-task","--list-projects"])
    except getopt.GetoptError:
        helpText()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            helpText()
            sys.exit()
        elif opt in ("-p", "--project"):
            projectName = arg.strip()
        elif opt in ("-l", "--list-tasks"):
            action = 'list-tasks'
        elif opt in ("-s", "--list-projects"):
            action = 'list-projects'

        elif opt in ("-n", "--new-task"):
            verbose = 1

    # if len(sys.argv) < 2:
    #     helpText()
    #     sys.exit()

    introText()

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

    if action == 'list-projects':
        projectsData = apiGetProjects()
        printProjects(projectsData)
        sys.exit(2)


if __name__ == "__main__":
	main(sys.argv[1:])

