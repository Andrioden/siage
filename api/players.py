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
        self.response.headers['Content-Type'] = 'application/text'

        players_data = []
        for player in Player().query(Player.nick == request_data['nick']):
            players_data.append(player.get_data())

        # CHECK IF PLAYER EXISTS
        if(players_data):
            self.response.write('Nickname is taken')
            self.response.set_status(403)

        # PLAYER DOES NOT EXIST. SAVE PLAYER
        else:
            Player(nick = request_data['nick']).put()
            self.response.out.write("Player " + request_data['nick'] + " saved successfully")

class PlayerHandler(webapp2.RequestHandler):
    def get(self, player_id):
        logging.info("Returning data for player_id: %s", player_id)
        
        # BUILD DATA
        players_data = "";
        if(player_id.isdigit()):
            player = Player.get_by_id(int(player_id))
        else:
            for player in Player().query(Player.nick == player_id):
                players_data = player.get_data()

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
    (r'/api/players/(\S+)', PlayerHandler)
], debug=True)