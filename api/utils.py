import json
from google.appengine.api import users
from models import Player

def error_400(response, code, message):
    response.headers['Content-Type'] = 'application/json'
    response.set_status(400)
    response.out.write(json.dumps({'error_code': code, 'error_message': message}))

def unauthorized_401(response, code, message):
    response.headers['Content-Type'] = 'application/json'
    response.set_status(401)
    response.out.write(json.dumps({'error_code': code, 'error_message': message}))

def forbidden_403(response, code, message):
    response.headers['Content-Type'] = 'application/json'
    response.set_status(403)
    response.out.write(json.dumps({'error_code': code, 'error_message': message}))

def validate_logged_in(response):
    user = users.get_current_user()
    if not user:
        unauthorized_401(response, "VALIDATION_ERROR_NOT_LOGGED_INN", "The browsing user is not logged in.")
        return False
    elif not Player.query(Player.userid == user.user_id()).get():
        unauthorized_401(response, "VALIDATION_ERROR_NOT_AUTHENTICATED", "The browsing user is logged in, but not authenticated.")
        return False
    return True

def validate_logged_in_admin(response):
    if not validate_logged_in(response):
            return
    if not users.is_current_user_admin():
        forbidden_403(response, "VALIDATION_ERROR_MISSING_ADMIN_PERMISSION", "The browsing user is logged in and authenticated, but does not have admin permissions.")
        return False

    return True