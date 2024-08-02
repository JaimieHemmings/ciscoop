# CI/Scoop

CI/Scoop was developed as for me as a developer to share my thoughts, opinions and projects. Users are able to register an account and send messages to me using the form on the contact page. As an admin of the site I am able to Create, Edit and Delete blog posts. The website employs a feature rich content editor for use with writing blog posts allowing the use of font sizing, italics, bold fonts, lists, externally hosted images etc.

![Preview of Website](documentation/img/preview.jpg)

View the website [here](https://ciscoop-46d70b5281a0.herokuapp.com/).

# Project Overview

CI/Scoop is blogging website built using **Python**, **Flask**, **SQLAlchemy**, **Bootstrap 5**, and **JavaScript**.

- User authentication and CRUD functionality is handled by a relational backend database (**PostgreSQL**)

CI/Scoop is my submission for the Milestone 3 Project by Code Institute in partnership with East Kent College for the Level 5 Diploma in Full Stack Web Application Development.

The choice to make this project was influenced by my need for a blogging platform to highlight my projects and knowledge in full stack web application by creating a portfolio website, thereby the website itself is a demenstration of my abilities.

<details>
<summary>Table of Contents</summary>
- Add
- table
- of
- contents
- here
</details>

# UX Development

## Strategy

### Project Goals

- Develop a full stack website
- Website needs to include full CRUD functionality
- Guests will be able to view and navigate public sections of the website
- Guests will be able to send a message to the admins using the form on the contact page
- Admins will be able to create, edit and delete blog posts
- Admins will be able to read and delete messages sent by the contact form
- Present information in an easy to read manner
- Implement responsive design methodologies
- Provide the option for users to create an account and login/logout
- Provide registered Admin users CRUD functionality in appropriate sections of the website
- Implement defensive programming to prevent accidental deletion of data
- Handle errors to aid the users in understanding the cause of the issue and getting them back on track

### User Demographic

- Anyone interested in technology or software development
- Anyone interested in my progress as a full stack developer
- potential employers

### User Stories

#### First Time Visitor Goals

As a first time visitor I want to be able to:

- Immediately understand the purpose of the website
- Immediately recognise how to use and navigate the website
- Browse the articles available
- Register for an account

#### Registered/Returning Visitor Goals

As a registered or returning visitor I want to be able to:

- Easily find new content
- Send a message to the site owner/admin
- Browse new blog posts

#### Site Admin Goals

As a site admin I want to be able to:

- Be able to add a new blog post
- Be able to edit exisiting blog posts
- Be able to delete exisiting blog posts
- View messages sent via the contact form
- Delete messages sent via the contact form

### Scope

#### Functionality Planning

When planning the scope of the project I created a Viability Analysis of the features I wished to add. This would allow me to prioritise the most critical features and defer the development of lesser functionality to a later date. Below is that table:

| #   | Feature                                | Importance | Viability |
| --- | -------------------------------------- | ---------- | --------- |
| 1   | View, Create, Edit & Delete Blog Posts | 5          | 5         |
| 2   | Registration Functionality             | 5          | 5         |
| 3   | Login/Logout Functionality             | 5          | 5         |
| 4   | Contact Form                           | 5          | 5         |
| 5   | Read/Delete Contact Form Submissions   | 5          | 5         |
| 6   | Blog Commenting Functionality          | 2          | 5         |
| 7   | Display Suggested Articles             | 1          | 2         |
| 8   | Share Blog Posts on Social Media       | 2          | 4         |
| 9   | Log User Activity                      | 2          | 2         |
| 10  | User Profile Page Functionality        | 2          | 5         |
| 11  | Search for Blog Posts                  | 1          | 4         |
| 12  | User Action Validation                 | 5          | 5         |

Based on the premise of creating a minimally viable product I have decided to focus on implementing only the core functionality for the application to meet the minimum required specifications for functionality. This means on the initial development sprint I will be implementing features 1, 2, 3, 4, 5 and 12.

### Functionality Requirements

- Clean and thematically cohesive design
- Functional and aesthetic presentation of blog posts
- Login/logout functionality
- Full CRUD functionality
- Defensive programming usage to safeguard the database from malicious or erroneous input
- Appropriate handling of error messages

# Create Virtual environment

To create a virtual environment for the project open gitbash or CLI of your choice within the project directory. To do this follow the instructions below:

- Open the CLI in the project directory
- Type `python -m venv /virt`

Then to run the virtual environment type:

- `.\\virt\Scripts\Activate`

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

If you need to set the Flask app environment variable simply run the command:

- `$env:FLASK_APP="app.py"`
