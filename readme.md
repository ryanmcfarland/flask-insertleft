# Personal Flask Website - insertleft

Weblink - www.insertleft.com

## Description

A personal website that was built using a flask backend and a bootstrap frontend that hosts the ability to create and edit role-playing sheets for the custom game "Shootouts & Sheriffs" and the post blog entries to the front-page. 

Still a work in progress, looking for feedback

## Setup & Startup

Envirnoment variables to be created for the app

``` Required Variables
SECRET_KEY
FLASK_ENV
MAIL_USERNAME
MAIL_PASSWORD
FLASK_APP
DATABASE_URL
ADMIN
```

Create python virtual env and install requirements.txt

```
python -m venv wsenv
pip install -r requirements.txt
```

To set-up the app's db on start-up

``` Create and start flask
flask db init
flask db migrate
flask db upgrade
flask run
```

On the first request to the flask app, the app will:

1. Insert Admin, power and User into the role db if not already present
2. create an admin account with an randomly generated password and send to the admin email
3. Assign Admin account with Admin role if not already mapped

## Custom Flask Click Commands

```
flask create-user --username test --email test1
flask create-role --role Test
flask append-role --username test --role Test
```

## Models

1. User

Use flask-login UserMixin and some custom functions to check the link posts, sheet and user roles

2. Role

Each user can have a role attached to them. the decorator, @role_required is used to check if the user has access to the underlying route

3. Entry

A blog post model, contains usual columns for each blog post

4. Weapon & Sheet

Used with the shootout blueprint. Weapon holds weapons that can be attached to each player's character sheet. Each sheet contains the stats for each player character.

## Working Modules - Flask Blueprints

### Auth

Simple routes to login, logout and register users within the app.

### Common

Includes click comamnds, decorators and other utility functions used within the flask app.

### Shootout

Blueprint that holds all the routes to the shootout game. These routes lets a registered user create a form fillable character sheet that only they or admins can edit and delete. They can show the sheet to other users.

*The shootout home page:*

![image](https://user-images.githubusercontent.com/32989131/120724516-e7b90680-c4cb-11eb-8b02-e7b1bf1587cb.png)

*The shootout edit page:*

![image](https://user-images.githubusercontent.com/32989131/120724648-251d9400-c4cc-11eb-9d05-f11070a67c3f.png)

### Contact

Routes to a cv download and a mailto address

### Main

Routes to the home page and blog page. If you are admin user, lets you access the admin page that will let you publish, edit, preview and delete existing posts. The admin page will highlight unpublished articles as yellow.

*Blog Admin Page:*

![image](https://user-images.githubusercontent.com/32989131/120724099-08349100-c4cb-11eb-99cc-9f4a11c236cb.png)

*Blog articles with pagination:*

![image](https://user-images.githubusercontent.com/32989131/120724742-55653280-c4cc-11eb-9249-2e6c02f94317.png)

## Personal Notes

I followed the below guides for help and context when trying to build this from scratch:
- Miguel Grinberg's flask turotial - [Flask Mega Turotial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- Corey M Schafer's flask guide - [Corey's github](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog)
- Charles Leifer - [How to make a blog in an hour](https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/)

## TODO

- Update to flask 2.0 and Bootstrap 5.0
- Easy way to view other user's sheets
- implement popover events to add tags to articles
- Coloured Model headings - https://bootsnipp.com/snippets/dzvv
- better styling?


### Misc Notes

- A potential way to grab first element of a parsed markdown element maybe?
```
>> "\n".join(res[:2])
'### Flask\r\nFlask is a **web** framework for _Python_.\r'
>>> res=Notes.query.all()[1].note.split("\n")
>>> res
['### Flask\r', 'Flask is a **web** framework for _Python_.\r', '\r', 'Here is the Flask logo:\r', '\r', '![Flask Logo](https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png)']
```

- dyanmic way to adjust size of bootstrap nested column

This is used within the shootout sheet to get weapons and notes the same size if large elements

https://stackoverflow.com/questions/40012682/how-to-divide-bootstrap-col-md-div-to-half-vertically/40012791

https://stackoverflow.com/questions/24325744/bootstrap-custom-popover
