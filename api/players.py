#!/usr/bin/env python

import webapp2
import json
import logging
from models import Player

class PlayersListHandler(webapp2.RequestHandler):
    def get(self):
        # BUILD DATA
        players_data = []
        for player in Player().query():
            players_data.append(player.get_data())
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(players_data))

    def post(self):
        # PROCESS REQUEST
        request_data = json.loads(self.request.body)
        Player(nick = request_data['nick']).put()
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("POST (Save) received with data: " + self.request.body)

class PlayerHandler(webapp2.RequestHandler):
    def get(self, player_id):
        logging.info("Returning data for player_id: %s", player_id)
        
        # BUILD DATA 
        player = Player.get_by_id(int(player_id))
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        if player:
            self.response.out.write(json.dumps(player.get_data()))
        else:
            self.response.out.write(json.dumps({'data': player}))

    def put(self, playerId):
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("PUT (Update) received with data: " + self.request.body)

app = webapp2.WSGIApplication([
    (r'/api/players/', PlayersListHandler),
    (r'/api/players/(\d+)', PlayerHandler),
], debug=True)