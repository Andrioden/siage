#!/usr/bin/env python

import webapp2
import json

class PlayersHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'   
        obj = [
            {'nick': 'Andrioden', 'rating': 1600, 'winrate': '55', 'bestcivilization': 'Huns'},
            {'nick': 'Shrubber', 'rating': 1500, 'winrate': '51', 'bestcivilization': 'Mongols'}
        ]
        self.response.out.write(json.dumps(obj))

app = webapp2.WSGIApplication([
    ('/api/players', PlayersHandler),
    ('',PlayersHandler)
], debug=True)