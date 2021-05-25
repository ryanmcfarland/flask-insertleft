from app import db
from app.models import Role
from app.common import bp

# Create User Role if not already part of the database
@bp.before_app_first_request
def add_roles_on_startup():
    for i in ["Admin", "Power", "User"]:
        i=i.capitalize()
        r = Role.query.filter_by(name=i).first()
        if not r:
            r = Role(name=i)
            db.session.add(r)
            db.session.commit()
            print("Added Role: "+i)
        else:
            print("Role added already: "+i)
