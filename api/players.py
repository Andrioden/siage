#!/usr/bin/env python

import webapp2
import json
import logging
from models import Player
from utils import error_400

class PlayersHandler(webapp2.RequestHandler):
    def get(self): 
        """ GET PLAYERLIST """
        # BUILD DATA
        players_data = [player.get_data() for player in Player().query()]
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(players_data))

    def post(self): 
        """ CREATE PLAYER """
        request_data = json.loads(self.request.body)
        nick = request_data['nick']
        
        existing_player_with_nick = Player.query(Player.nick == nick).get()
        if existing_player_with_nick:
            error_400(self.response, "NICK_TAKEN", "Nick %s is taken" % nick)
        else:
            Player(nick = nick).put()
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps({'response': "Player " + request_data['nick'] + " saved successfully"}))

class PlayerHandler(webapp2.RequestHandler):
    def get(self, player_id_or_nick): 
        """ GET SINGLE PLAYER """
        logging.info("Returning data for player_id_or_nick: %s", player_id_or_nick)
        
        # BUILD DATA
        if player_id_or_nick.isdigit():
            player = Player.get_by_id(int(player_id_or_nick))
        else:
            player = Player.query(Player.nick == player_id_or_nick).get()
            
        # RETURN RESPONSE
        if player:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(player.get_data()))
        else:
            self.response.out.write(json.dumps({'error': "PLAYER_NOT_FOUND"}))

    def put(self, player_id_or_nick): 
        """ UPDATE SINGLE PLAYER """
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("PUT (Update) received with data: " + self.request.body)

app = webapp2.WSGIApplication([
    (r'/api/players/', PlayersHandler),
    (r'/api/players/(\d+)', PlayerHandler),
    (r'/api/players/(\S+)', PlayerHandler)
], debug=True)