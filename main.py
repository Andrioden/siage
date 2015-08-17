#!/usr/bin/env python

"""
The the only purpose of this file is to handle the root access to the site
like si-age-league.appspot.com. By serving the index.html.
"""

import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
        
app = webapp2.WSGIApplication([
    ('/.*', MainHandler),
], debug=True)