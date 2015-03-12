#!/usr/bin/env python

import webapp2
from rating import recalculate_ratings

class RecalcHandler(webapp2.RequestHandler):
    def get(self):
        recalculate_ratings()
        self.response.write("OK")

app = webapp2.WSGIApplication([
    (r'/admin/recalc/', RecalcHandler),
], debug=True)