This project is a very simple starter social media webiste where you can use and edit if you want to improve it. 
So far you can register, login,create posts, edit posts, and delete posts.



Post Class:
Table Name: "posts"
Columns:
id (Integer, Primary Key)
text (String, max length 4096)
poster's id (Integer, Foreign Key referencing "poster.id")
Relationship: One-to-Many with Poster class
Poster Class:

Columns:
id (Integer, Primary Key)
username (String, unique, max length 250)
password (String, max length 250)
Relationship: One-to-Many with Post class

These are the only classes that are in use for now maybe in the future a like and
comment button will be added to elevate this website.

/register:

GET: Render the registration form
POST: Register a new user, hash the password, and redirect to login page
/login:

GET: Render the login form
POST: Authenticate user, set session, and redirect to homepage
/logout:

Log out user and redirect to homepage
/homepage:

Display all posts on the homepage
/add_post:

GET: Render form to add a new post
POST: Add a new post, link it to the current user, and redirect to homepage

/edit_post/<id>:

GET: Render form to edit a specific post
POST: Update the text of the post and redirect to homepage
/delete_post/<id>:

Delete a specific post if the current user is the author
/register:

GET: Render the registration form
POST: Register a new user, hash the password, and redirect to login page
/login:

GET: Render the login form
POST: Authenticate user, set session, and redirect to homepage
/logout:

Log out user and redirect to homepage
/homepage:

Display all posts on the homepage

/add_post:

GET: Render form to add a new post
POST: Add a new post, link it to the current user, and redirect to homepage

/edit_post/<id>:

GET: Render form to edit a specific post
POST: Update the text of the post and redirect to homepage

/delete_post/<id>:

Delete a specific post if the current user is the author
The Recent posts show all the new posts that have just been made
Users can add new posts as long as your'e logged in

.post style , .post-header, .post-footer, and .button all 
give the boxes a nicer looking detail to ensures that it can pop more





HOW TO RUN:
Make sure you have the right imports instaled if you dont the code wont work here are the imports you need to install:
import math
from flask import Flask, render_template,request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from socket import gethostname
from flask_login import (LoginManager, UserMixin,
    login_user, logout_user, login_required, current_user)
from datetime import datetime
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
    )

After that you can copy and paste the code and templates into pythonanywhere and 
make sure to press the green save button and you'll be set
This code sets up the database tables and runs the Flask application.
The application creates an admin user and a sample post for testing purposes.








