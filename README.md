# CI/Scoop

# Create Virtual environment

To create a virtual environment for the project open gitbash or CLI of your choice within the project directory. To do this follow the instructions below:

- Open the CLI in the project directory
- Type `python -m venv /virt`

Then to run the virtual environment type:

- `\virt\Scripts\Activate`

This process varies depending on your local development environment and operating system. If the above doesn't work you may need to search for instructions specific to your development environment. Please ensure you have Python installed.

# Create and migrate Database

To create the database enter the CLI and type:

- `psql` and log in with your admin credentials
  - You may need to change username with `psql -U "username"`
  - It will then ask for a password for that username
- `CREATE DATABASE database_name;`

In order to run the migrations you will need to then type the following:

- `$ python`
- `>>> from ciscoop import app, db`
- `>>> app.app_context().push()`
- `>>> db.create_all()`
