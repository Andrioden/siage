import json
from google.appengine.api import users
from models import Player
from datetime import datetime


def error(status, response, code, message):
    response.headers['Content-Type'] = 'application/json'
    response.set_status(status)
    response.out.write(json.dumps({'error_code': code, 'error_message': message}))


def unauthorized_401(response, code, message):
    error(401, response, code, message)


def forbidden_403(response, code, message):
    error(403, response, code, message)


def validate_authenticated(response):
    user = users.get_current_user()
    if users.is_current_user_admin():
        return True
    elif not user:
        unauthorized_401(response, "VALIDATION_ERROR_NOT_LOGGED_INN", "The browsing user is not logged in.")
        return False

    player = Player.query(Player.userid == user.user_id()).get()
    if not player:
        unauthorized_401(response, "VALIDATION_ERROR_NOT_CLAIMED", "The browsing user is logged in with google account, but have not claimed a player.")
        return False
    elif not player.verified:
        unauthorized_401(response, "VALIDATION_ERROR_NOT_VERIFIED", "The browsing user has not been verified, the player claim has not been verified by an admin.")
        return False
    return True


def validate_logged_in_admin(response):
    if not users.is_current_user_admin():
        forbidden_403(response, "VALIDATION_ERROR_MISSING_ADMIN_PERMISSION", "The browsing user is logged in and authenticated, but does not have admin permissions.")
        return False
    else:
        return True


def validate_request_data(response, request_data, list_of_dict_keys):
    for key in list_of_dict_keys:
        if request_data.get(key, None) in [None, '']:
            error(400, response, "VALIDATION_ERROR_MISSING_DATA", "The request data is missing the input value '%s'" % key)
            return False
    return True


def current_user_player():
    user = users.get_current_user()
    return Player.query(Player.userid == user.user_id()).get()


def date_to_epoch(date_value):
    return int((date_value - datetime(1970,1,1)).total_seconds())


def set_json_response(response, data):
    response.headers['Content-Type'] = 'application/json'
    response.out.write(json.dumps(data))