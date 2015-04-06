import webapp2
import json
import logging
from models import Player
from google.appengine.api import users

class UserHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        user = users.get_current_user()
        if user:
            player = Player.query(Player.userid == user.user_id()).get()
            player_nick = player.nick if player else None
            user_data = { 'user_name': user.nickname(), 'logged_in': True,  'player': player_nick, 'is_admin': users.is_current_user_admin() };
            self.response.out.write(json.dumps(user_data))
        else:
            self.response.out.write(json.dumps({}))
        
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
