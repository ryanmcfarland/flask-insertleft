import re
import markdown

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

## Many-to-many relationship table between user and role
## allows for a user to have multiple roles
user_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

# User class, maps the user to multiple sheets, roles and blog entries
# Users can have multiple roles
# backref enables the Sheet/Posts model to access the user via sheet.author.id
# lowercase_username is a hybrid property and not a column, used to verify that username strings
# are not duplicated regardless of case (see offical sqlalchemy notes)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    verified = db.Column(db.Boolean, default=False)
    roles = db.relationship("Role", secondary=user_permissions, backref=db.backref('user_permissions', lazy='dynamic'),lazy='dynamic')
    shootout_sheets = db.relationship('ShootoutSheet', backref='author', lazy='dynamic')
    beatcops_sheets = db.relationship('BeatCopsSheet', backref='author', lazy='dynamic')
    swn_sheets = db.relationship('StarsSheet', backref='author', lazy='dynamic')
    posts = db.relationship('Entry', backref='author', lazy='dynamic')

    @hybrid_property
    def lowercase_username(self):
        return self.username.lower()
    
    @lowercase_username.expression
    def lowercase_username(cls):
        return func.lower(cls.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # enfore role list and return true or false
    def check_roles(self, roles):
        if not isinstance(roles, (list, tuple)):
            roles = [roles]
        return any (x in roles for x in self.get_roles())

    # loop through role values and print out list of roles attached to the user
    def get_roles(self):
        return [r[0] for r in  self.roles.values('name')]

    def append_role(self, role):
        r = Role.query.filter(Role.name.in_([role])).first()
        if not r:
            return None
        elif not self.check_appended_role(r):
            self.roles.append(r)

   
    def remove_role(self, role):
        r = Role.query.filter(Role.name.in_([role])).first()
        if not r:
            return None
        elif self.check_appended_role(r):
            self.roles.remove(r)


    def check_appended_role(self, role):
        return self.roles.filter(user_permissions.c.role_id == role.id).count() > 0   

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        self.name=self.name.capitalize()

    def __repr__(self):
        return '<Role {}>'.format(self.name)


## Many-to-many relationship table between tag and entry
attached_tags = db.Table('attached_tags',
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


#https://github.com/eugenkiss/Simblin/blob/master/simblin/models.py
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, default="")
    slug = db.Column(db.String, unique=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    caption = db.Column(db.Text, default="")
    content = db.Column(db.Text, default="")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship("Tag", secondary=attached_tags, backref=db.backref('attached_tags', lazy='dynamic'), lazy='dynamic')

    def output_md(self):
        self.content=markdown.markdown(self.content, extensions=['attr_list', 'fenced_code'])
    
    def output_snapshot(self, snapshot):
        self.content="\n".join(self.content.split("\n")[:snapshot])
        
    def gen_slug(self):
        self.slug = re.sub(r'[^\w]+', '-', self.title.lower()).strip('-')
    
    # If False, always set published to False, return True for upstream checks
    # If true, check contents and return False if any fields empty
    # else set columns and return
    def publish(self, publish=True):
        if not publish:
            self.published=publish
            return True
        elif not self.title or not self.caption or not self.content:
            return False
        else:
            self.published=publish
            self.gen_slug()
            self.publish_date = datetime.utcnow()
            return True

    def __repr__(self):
        return '<Entry {}>'.format(self.title)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
