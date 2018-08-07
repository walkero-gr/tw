**tw** is a python script that can be used to get information from [Teamwork PM](http://teamworkpm.net/) to your terminal. It uses the [Teamwork Projects API](https://developer.teamwork.com/projects/introduction/welcome-to-the-teamwork-projects-api) to get the information and print them.

Currently the script can:
- show the Projects the user has access to
- show the Tasks of a given project
- show basic information of a given task ID


### Usage
Before you use the script you have to edit it and add the your teamwork site name and your API key. To find the values you have to insert, please read [Finding your API Key & URL](https://developer.teamwork.com/projects/finding-your-url-and-api-key/api-key-and-url) at Teamwork documentation.

The above values should be entered at the following lines of the script, by replacing the dummy values.

```python
company = "YOUR_TEAMWORK_SITE_NAME"
key = "YOUR_API_KEY"
```
As soon as you save the script you are good to go. Open a terminal and run the script using 
```bash
tw.py [-h,-l,-s,-i] -p <projectName> -t <taskID>
```

#### Parameters and Actions
```bash
    tw.py [-h,-l,-s,-i] -p <projectName> -t <taskID>
    
    -h      Returns this help text

    Parameters
    ----------
    -p|--project    The project name
    -t|--task-id    The task ID

    Actions
    -------
    The latest action overrides the previous defined, f.ex. if you give -l -s then only -s will be executed.
    -l|--list-tasks     List tasks of the project. The project name parameter is mandatory.
    -s|--list-projects  List the available projects you have access to.
    -i|--task-info      Show information about the specified task. The task ID parameter is mandatory.
```
