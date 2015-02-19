#!/usr/bin/env python

import webapp2
import json

class PlayersHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'   
        obj = [
            {'nick': 'Andrioden', 'rating': 1600},
            {'nick': 'Shrubber', 'rating': 1500}
        ]
        self.response.out.write(json.dumps(obj))

app = webapp2.WSGIApplication([
    ('/ajax/players', PlayersHandler)
], debug=True)