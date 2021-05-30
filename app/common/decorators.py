from functools import wraps
from flask_login import current_user 
from werkzeug.exceptions import Forbidden

# User has role in this list provided
#from app.common.decorators import role_required
# @role_required("Admin") | @role_required(["Admin", "Power"])
def role_required(roles):
    """
    Takes a role (a string name singular or list) and checks if the User has the role assigned
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if current_user.check_roles(roles):
                return func(*args, **kwargs)
            else:
                raise Forbidden("You do not have access")
        return inner
    return wrapper