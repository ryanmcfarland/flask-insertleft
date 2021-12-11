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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
