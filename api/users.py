import webapp2
import json
import logging
from models import Player
from google.appengine.api import users
from utils import error_400


class UserHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        existing_player = Player.query(Player.userid == user.user_id()).get()
        if user:
            user_data = { 'user_name': user.nickname(), 'logged_in': True,  'player': existing_player.nick};            
        else:
            return error_400(self.response, "VALIDATION_ERROR_NOT_LOGGED_INN", "The browsing user is not logged inn.")

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(user_data))

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        return webapp2.redirect(users.create_login_url())

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        return webapp2.redirect(users.create_logout_url('/'))


app = webapp2.WSGIApplication([
    (r'/api/users/me', UserHandler),
    (r'/api/users/login', LoginHandler),
    (r'/api/users/logout', LogoutHandler)
], debug=True)
