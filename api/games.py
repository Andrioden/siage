#!/usr/bin/env python

import webapp2
import json
import logging
import models

class GamesListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = [
            {'id:': 1},
            {'id': 2}
        ]
        self.response.out.write(json.dumps(obj))

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Game saved"}))

class GameHandler(webapp2.RequestHandler):
    def get(self, game_id):
        logging.info("Returning data for game_id: %s", game_id)

        self.response.headers['Content-Type'] = 'application/json'
        obj = {'game_id': game_id}

        self.response.out.write(json.dumps(obj))

    def put(self, gameId):
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("PUT (Update) received with data: " + self.request.body)


app = webapp2.WSGIApplication([
    (r'/api/games/', GamesListHandler),
    (r'/api/games/(\d+)', GameHandler),
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