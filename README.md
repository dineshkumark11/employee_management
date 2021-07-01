# employee_management_system
Employee management - Django
## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/nobitadore/employee_management.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3.7 -m venv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies:

```sh
(env)$ cd employee_management/
(env)$ python3.7 manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
