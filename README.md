# python-project-template
A python project template for educational purposes.

This project serves 2 purposes:
1. To be used as a base template for python projects
2. To help people understand the testing, linting, CI etc. python stack by **cloning/forking it and breaking it.**

## Quickstart
1. Create a python virtual environment:  
`python -m venv .venv`
2. Activate your environment:  
`source .venv/bin/activate`
3. If you want install the development requirements:  
`pip install -r requirements.dev.txt`
4. Install pre-commit to use pre-commit hooks:
`pre-commit install`
5. Install the package in development mode:  
`pip install -e .`

OR

1. `make environment`
2. `source .venv/bin/activate`

## Python venv
**venv** stands for virtual environment and is part of the python standard library (i.e. you don't have to install it).
Python virtual environments' role is to create an isolated python environment for each project so that there are no dependency issues etc. from conflicting project requirements (e.g. Project A need pandas 1.0 and Project B needs pandas 1.1).  

The terminal command `python -m venv .venv` creates a directory call .venv.  
You can activate the virtual environment with `source .venv/bin/activate`. 

To enable the new venv in jupyter notebooks follow the instructions here:  
https://janakiev.com/blog/jupyter-virtual-envs/

link to the venv documentation:  
https://docs.python.org/3/library/venv.html

Alternatives to venv are conda environments but there are some big differences between the 2: 
https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

## requirements.txt
Requirements files specify the dependencies of the project for other packages.  
How the requirements are distributed across directories and files varries.  
For this project we have 3 files where the requirements are stored: 
* [requirements.dev.txt](requirements.dev.txt) has the dependencies anything that is necessary for the developer but not the user of the package (e.g. testing & linting)
* [docs/requirements.txt](docs/requirements.txt) has the dependencies for building the documentation.
* [setup.py](setup.py) has the **examplepackage** dependencies as part of the `install_requires` parameter of the `setup` function. More info in the dedicated section below.  

The terminal command `pip installs -r requirements.txt` install requirements from the specified file.

Alternatives to using requirements.txt files are conda enviroment yaml files (if you choose to use a conda env that is): 
https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

## Pre-commit hooks
[Git hooks](https://git-scm.com/docs/githooks) are programs you can place in a hooks directory to trigger actions at certain points in git’s execution. 
[Pre-commit](https://pre-commit.com/) is a handy tool that manages the installation and execution of any hook written in any language before every commit.  

We can configure pre-commit hooks in the [.pre-commit-config.yaml](.pre-commit-config.yaml) file. For this template we check the linting with *flake8* and the docs with *pydocstyle*. And code cannot be committed unless it passes those checks.  

To install pre-commit: 
1. `pip install pre-commit`
2. with your venv activated `pre-commit install`

To bypass the pre-commit checks you can commit your changes with the --no-verify option.  
`git commmit -m "description" --no-verify`

## flake8
flake8 checks if the code is uggly according to [PEP8](https://www.python.org/dev/peps/pep-0008/).  

Quotting the the [flake8 documentation](https://flake8.pycqa.org/en/latest/manpage.html) directly:  
*"flake8 is a command-line utility for enforcing style consistency across Python projects. By default it includes lint checks provided by the PyFlakes project, PEP-0008 inspired style checks provided by the PyCodeStyle project, and McCabe complexity checking provided by the McCabe project. It will also run third-party extensions if they are found and installed."*

flake8 is part of the requirements.dev.txt file and can be installed with pip.
To run a flake8 check you simply execute the terminal command: 
`flake8 examplepackage` *or any other dir that contains python files* 

You can configure flake8 by adding a section for flake8 in the [setup.cfg](setup.cfg) file. For example you can choose to instruct flake8 to ignore certain errors or change the default line length.

## black
black makes sure the flake8 checks pass by autoformatting all the .py files.  

Quotting the the [black documentation](https://black.readthedocs.io/en/stable/?badge=stable) directly:  
*"Black makes code review faster by producing the smallest diffs possible. Blackened code looks the same regardless of the project you’re reading. Formatting becomes transparent after a while and you can focus on the content instead."*

Black is part of the requirements.dev.txt file and can be installed with pip.
To format a directory with black run the terminal command:  
`black examplepackage` or file.py etc. 

Black (like flake8) is configurable but through a .toml file (not setup.cfg) that is currently excluded from this template.

Some IDEs have format on save features and can be configured to use black:
* Visual studio code: https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0
* Pycharm: https://www.jetbrains.com/help/pycharm/reformat-and-rearrange-code.html

## pydocstyle
[pydocstyle](http://www.pydocstyle.org/en/stable/) is a static analysis tool for checking compliance with Python docstring conventions.
By using pydocstyle we make sure that all modules and functions have consistent and good documentation.  

pydocstyle is part of the requirements.dev.txt file and can be installed with pip.
To run a pydocstyle check you simply execute the terminal command: 
`pydocstyle examplepackage` *or any other dir that contains python files* 

You can configure pydocstyle by adding a section for it in the [setup.cfg](setup.cfg) file. For this template we're using the numpy documentation convention and we're choosing to ignore some specific standards (e.g. D400 - docstring should be in imperative mood)

## nbstripout
[nbstripout](https://github.com/kynan/nbstripout) strips out output from Jupyter notebooks
Here we're using it as a pre-commit hook and it's configured in the .pre-commit-config.yaml  

Here is a video showing the main functionalities -> https://www.youtube.com/watch?v=BEMP4xacrVc

## pytest
Quotting the the [pytest documentation](https://docs.pytest.org/en/6.2.x/index.html) directly:
*"The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries."*

The tests for the package live in the [examplepackage/tests](examplepackage/tests) directory. Files in the main directory and its subdirectories that start with test_ and end with .py are recognised by pytest as test containing files (more rules for discovery [here](https://docs.pytest.org/en/6.2.x/goodpractices.html#conventions-for-python-test-discovery)).

pytest is part of the requirements.dev.txt file and can be installed with pip.
To run a pytest check you simply execute the terminal command: 
`pytest examplepackage` *or any other dir that contains python files* 
 
## Sphinx documentation
[Sphinx](https://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation.
The [docs/](docs) diretory is where the configuration for sphinx lives. The dependencies for the docs are in [docs/requiremetns.txt](docs/requiremetns.txt).  
To build the documentation run the following: 
1. `cd docs` *to go to the docs directory*
2. `make html` *to make the html version of the docs* 

Sphinx has the automodule functionality that creates the documetation automatically from the docstrings for each module and function. 
If you add a new module and you want to generate the documentation automatically, you'll need to add the following test in [index.rst](docs/source/index.rst):
```
newmodule
=============

.. automodule:: examplepackage.newmodule
   :members:
```

The build directory that contains the html version of the docs is in the .gitignore and therefore not in the github repo. 

Sphinx has many functionalities so for more details read the official documentation. 

## setup.cfg
[setup.cfg](setup.cfg) has many roles, for this template we're using it to configure things like flake8 and pydocstyle.  

example syntax: 
```python
[flake8]
# inline with Black code formatter
max-line-length = 88
```

More details:  
* https://docs.python.org/3/distutils/configfile.html
* https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html

## setup.py
[setup.py](setup.py) is what makes the package here pip-installable. We also add the package dependencies there (e.g. pandas==1.0). 
Here is the a simple setup.py:  
```python
from setuptools import setup, find_packages

setup(
    name="examplepackage",
    version="x.x",
    packages=find_packages(),
    description="package description",
    author="author name",
    install_requires=[
        "numpy>=1.0",
        "pandas==1.0",
    ],
)
```

More details on the setupscript: 
* https://docs.python.org/3/distutils/setupscript.html
* https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html

## Installing a package in Development mode
`pip install -e .` or `pip install --editable .` installs the package in editable (development) mode. 
This is essential for development because the changes you make in the code are directly applied in the installed package without the need for re-installation.  
Usefull links:
* https://packaging.python.org/guides/distributing-packages-using-setuptools/#working-in-development-mode
* https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#development-mode

## .gitignore
The title is pretty self explanatory.  

.gitignore is a file where you can add files and directories that you want git to ignore. The [.gitignore](.gitignore) in this template has the typical content. For example .venv, the directory that contains the python virtual environment, should not be push to github and is in .gitignore. 

## Makefile
The [Makefile](Makefile) makes life a bit more simple by having some of the necessary commands ready to go.
Available commands for this template are: 
1. `make environment`, equivalent to:
 ```
 python -m venv .venv
 source .venv/bin/activate
 pip install -r requirements.dev.txt
 pip install -e .
 python -m ipykernel install --name=examplepackage
 jupyter kernelspec list
 pre-commit install
```
2. `make clean`, equivalent to: 
```
echo "> Removing virtual environment"
rm -r .venv
echo "> Uninstalling from jupyter"
jupyter kernelspec uninstall examplepackage
```
3. `make install`, equivalent to:
```
pip install -r requirements.dev.txt
pip install -e .
```
4. `make test`, equivalent to:
```
pytest examplepackage
```
5. `make lint`, equivalent to:
```
flake8 examplepackage
pydocstyle examplepackage
```

## Github Actions
From the official https://github.com/features/actions page:  
*"GitHub Actions makes it easy to automate all your software workflows, now with world-class CI/CD. Build, test, and deploy your code right from GitHub. Make code reviews, branch management, and issue triaging work the way you want."*

Github actions are configured in yaml files in the [.github/workflows](.github/workflows) directory. For this template we have a single file [.github/workflows](.github/workflows/buildtest.yml).  
This runs the following actions for every pull-request and every push to merge: 
1. code-quality: flake8
2. docs-quality: pydocstyle
3. build and test (with pytest) for all the combinations of the chosen operating systems and python versions. 
e.g. macos-latest and python 3.7, 3.8 

With this configuration, reviewers can instantly spot whether the code meets the minimum standards and passes the tests:
![image](https://user-images.githubusercontent.com/64217214/133000246-0239d1d5-eb8c-49d6-9479-ad7db96d9d36.png)

Github Actions and Azure pipelines have many similarities, read more here:  
https://docs.microsoft.com/en-us/dotnet/architecture/devops-for-aspnet-developers/actions-vs-pipelines

## Licences
Details about the mainstream OSS (Open source software) licences can be found here:  
https://opensource.org  

Wikipedia has nice/comprehensive comparison table here:  
https://en.wikipedia.org/wiki/Comparison_of_free_and_open-source_software_licences

## Coding patterns
Some resources for coding patterns and API design: 
* ["Designing Machine Learning Toolboxes: Concepts, Principles and Patterns"](https://arxiv.org/abs/2101.04938)   
*Franz J. Király, Markus Löning, Anthony Blaom, Ahmed Guecioueur, Raphael Sonabend*
* https://refactoring.guru/design-patterns/python

## TO-DOs:
- [X] Descriptions for each component
- [X] Add documentation using sphinx
- [ ] Add branch protection rules (only in PRO and Enterprise)
- [X] Add a Makefile for ease of use (make install; make test; make lint; make env?)
