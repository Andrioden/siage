#!/usr/bin/env python

"""
The the only purpose of this file is to handle the root access to the site
like si-age-league.appspot.com. By serving the index.html.
"""

import os
import webapp2
import jinja2
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            login_logout_a = ('<span>Welcome, %s!</span> (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
        else:
            login_logout_a = ('<a href="%s">Sign in or register</a>.' % users.create_login_url('/'))

        template = JINJA_ENVIRONMENT.get_template('index.html')
        data = {'login_logout_a': login_logout_a}
        self.response.write(template.render(data))
        
app = webapp2.WSGIApplication([
    ('/.*', MainHandler),
], debug=True)