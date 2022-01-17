# Information for Contributors

This README file contains all the necessary information to contribute to this project.

## How to use Django

This project uses Django and a remote MySQL connection. In the `.replit` file, you can see the command `python project/manage.py runserver 0.0.0.0:3000`. This command starts the django server. 

Inside the project folder is the django code itself. We have a codesphere folder which is the code for the app itself, an app folder which is the configuration of Django for this project, and a `manage.py` file which helps you manage the server. You can also use the command `django-admin` instead of running `manage.py`.

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


## How to use Nix
> Warning: Nix support on Replit is still under heavy development and is subject to change.

You've just created a new Nix repl. There's not much here yet but with a little work you can use it as the starting point for *ANYTHING*.

To get started there are 2 config files that you can use to customize the environment. To show them click the 3 dots menu button in the file tree and then click "Show config files".

* `replit.nix` - Configures the nix environment

This file should look something like the example below. The `deps` array specifies which Nix packages you would like to be available in your environment. You can search for Nix packages here: https://search.nixos.org/packages

```
{ pkgs }: {
	deps = [
		pkgs.cowsay
		pkgs.zig
	];
}
```

* `.replit` - Configures the run command

The run command in this file should look something like this. You can use any binary made available by your `replit.nix` file in this run command.

```
run = "cowsay Welcome to nix on Replit!"
```

Once both those files are configured and you add files for your language, you can run you repl like normal, with the run button.

Both the Console and Shell will pick up changes made to your `replit.nix` file. However, once you open the Shell tab, the environment will not update until you run `exit`. This will close out the existing `shell` process and start a new one that includes any changes that you made to your `replit.nix` file.

### Learn More About Nix

If you'd like to learn more about Nix, here are some great resources:

* [Getting started with Nix](https://docs.replit.com/programming-ide/getting-started-nix) - How to use Nix on Replit
* [Nix Pills](https://nixos.org/guides/nix-pills/) - Guided introduction to Nix
* [Nixology](https://www.youtube.com/playlist?list=PLRGI9KQ3_HP_OFRG6R-p4iFgMSK1t5BHs) - A series of videos introducing Nix in a practical way
* [Nix Package Manager Guide](https://nixos.org/manual/nix/stable/) - A comprehensive guide of the Nix Package Manager
* [A tour of Nix](https://nixcloud.io/tour) - Learn the nix language itself