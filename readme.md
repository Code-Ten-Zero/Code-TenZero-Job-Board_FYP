[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flaskmvc)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# User CLI Commands

### 1. List users in the database

```bash
$ flask user list
```


# Admin CLI Commands

### 1. Lists admins in the database

```bash
$ flask admin list
```

### 2. Adds an admin

```bash
$ flask admin add <username> <password> <email>
```

### 3. Approve or disapprove a job listing

```bash
$ flask admin toggle <listing_id>
```

# Alumni CLI Commands

### 1. Lists alumnis in the database

```bash
$ flask alumni list
```

### 2. Add an alumni object to the database

```bash
$ flask alumni add <username> <password> <email> <alumni_id> <contact> <firstname> <lastname> 
```

### 3. Subscribe an alumni object

```bash
$ flask alumni subscribe <alumni_id>
```

### 4. Add job categories for the user

```bash
$ flask alumni add_categories <alumni_id> <job_categories>
```

### 5. Applies an alumni to a job listing

```bash
$ flask alumni apply <alumni_id> <listing_title>
```

### 6. Sets the 'has_seen_modal' field for an alumni

```bash
$ flask alumni set_modal_seen <alumni_id>
```

# Company CLI Commands

### 1. Lists company in the database

```bash
$ flask company list
```

### 2. Add a company object to the database

```bash
$ flask company add <username> <company_name> <password> <email> <company_address> <contact> <company_website>
```

### 3. Show all notifications for a company

```bash
$ flask company notifications <company_name>
```

# Listing CLI Commands

### 1. Lists listings in the database

```bash
$ flask listing list
```

### 2. Add listing object to the database

```bash
$ flask listing add <title> <description> <company_name> <salary> <position> <remote> <ttnational> <desiredcandidate> <area> <job_categories>
```

### 3. Delete listing object from the database

```bash
$ flask listing delete <id>
```

### 4. Get all applicants for the listing

```bash
$ flask listing applicants <listing_id>
```

# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what heroku executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to heroku by clicking on the "Deploy to heroku" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
