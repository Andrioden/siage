#!/usr/bin/env python

import webapp2
import json
import models

class GamesListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = [
            {'gameId:': 1},
            {'gameId': 2}
        ]
        self.response.out.write(json.dumps(obj))

    def post(self):
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("POST (Save) received with data: " + self.request.body)


class GameHandler(webapp2.RequestHandler):
    def get(self, gameId):
        self.response.headers['Content-Type'] = 'application/json'
        obj = [
            {'gameId': 1}
        ]
        self.response.out.write(json.dumps(obj))

    def put(self, gameId):
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("PUT (Update) received with data: " + self.request.body)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/api/games/', handler=GamesListHandler, name='games'),
    webapp2.Route(r'/api/games/<gameId:(\d+)>', handler=GameHandler, name='game')
], debug=True)



"""
\d	Any digit, short for [0-9]
\D	A non-digit, short for [^0-9]
\s	A whitespace character, short for [ \t\n\x0b\r\f]
\S	A non-whitespace character, short for [^\s]
\w	A word character, short for [a-zA-Z_0-9]
\W	A non-word character [^\w]
\S+	Several non-whitespace characters
\b	Matches a word boundary where a word character is [a-zA-Z0-9_].
"""