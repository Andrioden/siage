import json
from google.appengine.api import users
from models import Player

def error_400(response, code, message):
    response.headers['Content-Type'] = 'application/json'
    response.set_status(400)
    response.out.write(json.dumps({'error_code': code, 'error_message': message}))

def validate_logged_inn(response):
    user = users.get_current_user()
    if not user:
        error_400(response, "VALIDATION_ERROR_NOT_LOGGED_INN", "The browsing user is not logged inn.")
        return False
    elif not Player.query(Player.userid == user.user_id()).get():
        error_400(response, "VALIDATION_ERROR_NOT_AUTHENTICATED", "The browsing user is logged inn, but not authenticated")
        return False
    return True