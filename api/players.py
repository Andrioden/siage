#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb
import json
import logging
from models import *
from utils import *


class PlayersHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET PLAYERLIST --------- """
        data_detail = self.request.get('data_detail', "simple")
        active_str = self.request.get('active', "")
        claimed = self.request.get('claimed', "").lower()

        # BUILD DATA
        player_query = Player.query()

        if active_str in ["true", "false"]:
            active = active_str == "true"
            player_query = player_query.filter(Player.active == active)

        players_data = [player.get_data(data_detail) for player in player_query]

        # RETURN RESPONSE
        set_json_response(self.response, players_data)

    def post(self):
        """ --------- CREATE PLAYER --------- """
        # VALIDATING
        if not validate_authenticated(self.response):
            return
        
        # Create player and return response
        request_data = json.loads(self.request.body)
        nick = request_data['nick']

        existing_player_with_nick = Player.query(Player.nick == nick).get()
        if existing_player_with_nick:
            error(400, self.response, "NICK_TAKEN", "Nick %s is taken" % nick)
        else:
            new_player = Player(nick = nick).put().get()
            data = {'response': "Player %s saved successfully" % new_player.nick, 'player': new_player.get_data()}
            set_json_response(self.response, data)


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
            set_json_response(self.response, player.get_data("full"))
        else:
            error(404, self.response, "GAME_NOT_FOUND", "Player with ID or nick '%s' not found" % player_id_or_nick)

    def put(self, player_id_or_nick):
        """ --------- UPDATE SINGLE PLAYER --------- """
        request_data = json.loads(self.request.body)

        # PROCESS REQUEST
        if player_id_or_nick.isdigit():
            player = Player.get_by_id(int(player_id_or_nick))
        else:
            player = Player.query(Player.nick == player_id_or_nick).get()

        require_admin = False

        if request_data.has_key('userid'):
            player.userid = request_data['userid']
            require_admin = True

        if request_data.has_key('verified'):
            player.verified = request_data['verified']
            require_admin = True

        if request_data.has_key('active'):
            player.active = request_data['active']
            require_admin = True

        if request_data.has_key('setting_default_trebuchet_allowed'):
            player.setting_default_trebuchet_allowed = request_data['setting_default_trebuchet_allowed']

        if request_data.has_key('setting_default_rule_id'):
            setting_default_rule_id = request_data['setting_default_rule_id']
            if setting_default_rule_id is None:
                player.setting_default_rule = None
            else:
                player.setting_default_rule = ndb.Key(Rule, int(setting_default_rule_id))

        if require_admin:
            if not validate_logged_in_admin(self.response):
                return

        player.put()

        set_json_response(self.response, player.get_data("simple"))


app = webapp2.WSGIApplication([
    (r'/api/players/', PlayersHandler),
    (r'/api/players/(.*)', PlayerHandler),
], debug=True)