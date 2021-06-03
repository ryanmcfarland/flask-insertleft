# Personal Flask Website - bigbowldata

## Description

A personal website that was built using a flask backend and a bootstrap frontend that hosts the ability to create and edit role-playing sheets for the custom game "Shootouts & Sheriffs" and the post blog entries to the front-page. 

Still a work in progress, looking for feedback

## Setup & Startup

Envirnoment variables to be created for the app

```Required Variables
SECRET_KEY
FLASK_ENV
MAIL_USERNAME
MAIL_PASSWORD
FLASK_APP
DATABASE_URL
ADMIN
```

To set-up the app's db on start-up

``` Create and start flask
flask db init
flask db upgrade
flask run
```
## Working Modules - Flask Blueprints

### Common

### Shootouts and Sheriffs

A registered user can create a form fillable sheet with

### Blog

## Personal Notes

I followed the below guides for help and context when trying to build this from scratch:
- Miguel Grinberg's flask turotial - [Flask Mega Turotial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- Corey M Schafer's flask guide - [Corey's github](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog)
- Charles Leifer - [How to make a blog in an hour](https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/)

## TODO

- View other user's sheets
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
