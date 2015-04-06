import webapp2
import json
import logging
from models import Player
from google.appengine.api import users
from utils import error_400


class UserHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:

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

