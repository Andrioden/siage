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


def player_from_user():
    user = users.get_current_user()
    return Player.query(Player.userid == user.user_id()).get()