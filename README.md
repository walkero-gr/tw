**tw.py** is a python script that can be used to get information from [Teamwork PM](http://teamworkpm.net/) to your terminal. It uses the [Teamwork Projects API](https://developer.teamwork.com/projects/introduction/welcome-to-the-teamwork-projects-api) to get the information and print them.

Features:
- show the Projects the user has access to
- show the Tasks of a given project
- show basic information of a given task ID
- get the task ID from the current GIT branch name
- get current user task from all the projects
- get a list of a project's tasklists
- create a new task and assign to specific people


### Usage
Before you use the script you have to edit it and add the your teamwork site name and your API key. To find the values you have to insert, please read [Finding your API Key & URL](https://developer.teamwork.com/projects/finding-your-url-and-api-key/api-key-and-url) at Teamwork documentation.

The above values should be entered at the following lines of the script, by replacing the dummy values.

```python
company = "YOUR_TEAMWORK_SITE_NAME"
key = "YOUR_API_KEY"
```
As soon as you save the script you are good to go. Open a terminal and run the script using 
```bash
tw.py [-h] [-p PROJECT_NAME] [-t TASK_ID] [-l TASKLIST_ID]
      [-bp BRANCH_PREFIX] [-lt] [-ll] [-mt] [-lp] [-ti] [-gb]
      [-ct CREATE_TASK] [--version]
```

To make it available from any folder on your Linux machine, you can edit the .bashrc file under your user home folder and add the following line at the end of the file.
```
export PATH=$PATH:</path/to/file>
```


#### Parameters and Actions
```bash
tw.py [-h] [-p PROJECT_NAME] [-t TASK_ID] [-l TASKLIST_ID]
      [-bp BRANCH_PREFIX] [-lt] [-ll] [-mt] [-lp] [-ti] [-gb]
      [-ct CREATE_TASK] [--version]

This is a python script that can be used to get information from Teamwork
Projects Management. More info at https://github.com/walkero-gr/tw

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT_NAME, --project PROJECT_NAME
                        set the project name
  -t TASK_ID, --task TASK_ID
                        set the task ID
  -l TASKLIST_ID, --tasklist-id TASKLIST_ID
                        set the tasklist ID
  -bp BRANCH_PREFIX, --branch-prefix BRANCH_PREFIX
                        set branch prefix, if any. Used with --git-branch.
  -lt, --list-tasks     list tasks of the project. The project name parameter
                        is mandatory.
  -ll, --list-tasklists
                        list tasklists of the project. The project name
                        parameter is mandatory.
  -mt, --my-tasks       list my tasks across all project.
  -lp, --list-projects  list the available projects you have access to.
  -ti, --task-info      show information about the specified task. The task ID
                        parameter is mandatory.
  -gb, --git-branch     show information about the task ID taken from the
                        current GIT branch name. If task ID parameter is set,
                        this action will be ignored.
  -ct CREATE_TASK, --create-task CREATE_TASK
                        create a new task. The tasklist ID parameter is
                        mandatory. The value must be like "title @assigned-users [description]"
  --version             show program's version number and exit
```

##### -gb, --git-branch Parameter
In case the user uses the Teamwork task ID numbers at his project branch names, he can use the parameter --git-branch, so that the tw.py script will get the task ID from the branch name. This is a really fast way to retrieve information for the branch he currently work on.

Have in mind, to use this paramater you have to be in a folder that is a git repository. 

##### -bp BRANCH_PREFIX, --branch-prefix BRANCH_PREFIX
This parameter is used with --git-branch, where the user can specify a prefix he uses on branch names, along with the task ID number, f.ex. TW-#. This is necessary, so that this prefix will be removed from the branch name, and the task id will be retrieved.

There is also a new variable at the start of the script, named **default_branch_prefix**, where the user can set a default branch prefix, which will be used when the --git-branch is used and the --branch-prefix is missing. The user can override it by setting a value at the --branch-prefix parameter.

##### -ct CREATE_TASK, --create-task CREATE_TASK 
This parameter is used to create a new task in a specific tasklist. So the parameter **-l TASKLIST_ID, --tasklist-id TASKLIST_ID** is mandatory.

The user can set the title, the description and the assigned users to the new task using the following syntax.
```bash
tw.py -l <tasklist id> -ct "title @assigned-users [description]"
```
- The **title** can be alphanumeric.
- The **assigned-users** must have the **@** in front and works only with the last name of the users. Multiple users can be separated by commas. In case the user wants to assign the new task to himself, the **me** value can be used.
- The **description** can be alphanumeric and has to be enclosed in brackets [].