### TBD

## Personal Notes

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
https://stackoverflow.com/questions/14494747/add-images-to-readme-md-on-github

python3 -m venv venv
pip install -r requirements.txt
pip install python-dotenv

-> create -> flask db init
-> add new columns -> flask db migrate -m "rename sheet"
-> update db -> flask db upgrade

u = User.query.get(1)
s = Sheet(name="Test", character_class="witch", background="rich", level=2, xp=1000, max_hp=40, current_hp=30, attack_bonus=2, system_strain=5, ac1=15, ac2=16, mental_save=8, evasion_save = 9, physical_save = 7, author=u)
db.session.add(s)
db.session.commit()


>> "\n".join(res[:2])
'### Flask\r\nFlask is a **web** framework for _Python_.\r'
>>> res=Notes.query.all()[1].note.split("\n")
>>> res
['### Flask\r', 'Flask is a **web** framework for _Python_.\r', '\r', 'Here is the Flask logo:\r', '\r', '![Flask Logo](https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png)']

# TODO

1. Roles -> https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/

# https://stackoverflow.com/questions/40012682/how-to-divide-bootstrap-col-md-div-to-half-vertically/40012791

# models
#https://stackoverflow.com/questions/31842159/get-a-list-of-values-of-one-column-from-the-results-of-a-query
#https://stackoverflow.com/questions/922774/check-if-input-is-a-list-tuple-of-strings-or-a-single-string


<!-- #https://stackoverflow.com/questions/35965321/flashing-message-in-flask-on-a-bootstrap-modal -->

<!--
<div class="container">
    <div class="py-5 text-center">
        <div class="alert alert-{{category}} alert-dismissible fade show"><strong>{{category|upper}}</strong> {{ message }}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        </div>
    </div>
</div>
--> 

