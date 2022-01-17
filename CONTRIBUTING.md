# Information for Contributors

This README file contains all the necessary information to contribute to this project.

## How to use Django

This project uses Django and a remote MySQL connection. In the `.replit` file, you can see the command `python project/manage.py runserver 0.0.0.0:3000`. This command starts the django server. 

Inside the project folder is the django code itself. We have a codesphere folder which is the code for the app itself, an app folder which is the configuration of Django for this project, and a `manage.py` file which helps you manage the server. You can also use the command `django-admin` instead of running `manage.py`.

For more information on Django, please visit the website django

### `project/app/`

In the directory `project/app/`, we see configuration files. The only important files here are `settings.py` and `url.py`. In `settings.py`, there are configuration variables that we won't need to change much. 

## Overall Information

### Adding a New URL Pattern
To add a new url pattern, go to `project/codesphere/urls.py` to add a new URL pattern related to our main `codesphere` site while on the other hand, you can go to `project/app/urls.py` if you want to add a URL pattern with admin panel functionalities.

### Adding files

#### HTML

To add an HTML file for the frontend of this site, procceed to `project/codesphere/templates` and add a HTML file in this directory.

#### CSS, JS, etc.

To add other files for the frontent of this site, you can go to `project/codesphere/static` to upload/create the files. Please note that to import the file, you will need to put the word static in the url pattern and then add the directory it is in. For example if we want to access the `codesphere/styles.css` file, then we would write `{% static 'codesphere/styles.css' %}` to access the file.

### Adding Models

To add a new model to this webpage, procceed to the directory `project/codesphere/models.py` and add the model there. Then, procceed to `project/codesphere/admin.py` and register the model by adding the following code:
`admin.site.register(models.[NAME])`

### Documenting 

For any code you write that is more complicated than receiving and request, and then rendering a page, you should write some comments on what the script is meant to do. There are 2 options to do it.
- First, you can write one lined code and describe what each section is doing.
- On the other hand, you can also write a large multilined comment in psuedo code before the code block to explain what you are doing.

# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the CHANGELOG.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in CHANGELOG.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at **support@codesphere.org**. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/