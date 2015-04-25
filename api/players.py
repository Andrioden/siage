#!/usr/bin/env python

import webapp2
import json
import logging
from models import Player
from utils import error_400, validate_logged_in, validate_logged_in_admin

class PlayersHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET PLAYERLIST --------- """
        data_detail = self.request.get('data_detail', "simple")

        # BUILD DATA
        players_data = [player.get_data(data_detail) for player in Player.query()]

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(players_data))

    def post(self):
        """ --------- CREATE PLAYER --------- """
        # VALIDATING
        if not validate_logged_in(self.response):
            return
        
        # Create player and return response
        request_data = json.loads(self.request.body)
        nick = request_data['nick']

        existing_player_with_nick = Player.query(Player.nick == nick).get()
        if existing_player_with_nick:
            error_400(self.response, "NICK_TAKEN", "Nick %s is taken" % nick)
        else:
            new_player = Player(nick = nick).put().get()
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps({'response': "Player %s saved successfully" % new_player.nick, 'player': new_player.get_data()}))


class PlayerHandler(webapp2.RequestHandler):
    def get(self, player_id_or_nick):
        """ --------- GET SINGLE PLAYER --------- """
        logging.info("Returning data for player_id_or_nick: %s", player_id_or_nick)

        # BUILD DATA
        if player_id_or_nick.isdigit():
            player = Player.get_by_id(int(player_id_or_nick))
        else:
            player = Player.query(Player.nick == player_id_or_nick).get()
        
        # RETURN RESPONSE
        if player:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(player.get_data("full")))
        else:
            self.response.out.write(json.dumps({'error': "PLAYER_NOT_FOUND"}))

    def put(self, player_id_or_nick):
        """ --------- UPDATE SINGLE PLAYER --------- """

        if not validate_logged_in_admin(self.response):
            return

        # PROCESS REQUEST
        if player_id_or_nick.isdigit():
            player = Player.get_by_id(int(player_id_or_nick))
        else:
            player = Player.query(Player.nick == player_id_or_nick).get()

        userid = self.request.get("userid", None)
        if not userid == None:
            player.userid = userid

        verified = self.request.get("verified", None)
        if not verified == None:
            player.verified = (verified.lower() == "true")

        player.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(player.get_data("simple")))

app = webapp2.WSGIApplication([
    (r'/api/players/', PlayersHandler),
    (r'/api/players/(.*)', PlayerHandler),
], debug=True)