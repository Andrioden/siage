#!/usr/bin/env python

import webapp2
import json
import logging
from models import Game, Player, PlayerResult, PlayerResultStats
from datetime import datetime
from google.appengine.ext import ndb

PLAYER_RATING_START_VALUE = 1000

class GamesHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET GAMELIST --------- """
        self.response.headers['Content-Type'] = 'application/json'
        obj = [
            {'id': 1, 'game_type': "Game type 1"},
            {'id': 2, 'game_type': "Game type 2"}
        ]
        self.response.out.write(json.dumps(obj))

    #@ndb.transactional
    def post(self):
        """ --------- CREATE GAME --------- """
        request_data = json.loads(self.request.body)
        logging.info(request_data)
        
        """
        xx {u'map_style': u'typex', 
        xx u'resources': u'low', 
        u'playerResults': [
            {u'score': 6, u'team': 1, u'player_id': u'5629499534213120', u'civilization': u'Aztec', u'is_winner': True}, 
            {u'score': 8, u'team': 2, u'player_id': u'6296903092273152', u'civilization': u'Franks', u'is_winner': False}
        ], 
        xx u'starting_age': u'Castle Age', 
        xx u'population': 50, 
        xx u'game_type': u'GameType 1', 
        xx u'size': u'typex'}
        """
        # CREATE GAME OBJECT
        game_key = Game(
            # Settings from lobby Game Settings
#             size = request_data[''],
#             difficulty = request_data[''],
#             resources = request_data[''],
#             population = request_data[''],
#             game_speed = request_data[''],
#             reveal_map = request_data[''],
#             starting_age = request_data[''],
#             treaty_length = request_data[''],
#             victory = request_data[''],
#             team_together = request_data[''],
#             all_techs = request_data[''],
#             # Settings from Objective screen ingame
#             game_type = request_data[''],
#             map_type = request_data[''],
#             # Special settings
#             date = request_data[''],
#             duration_seconds = request_data[''],
#             trebuchet_allowed = request_data['']
        ).put()
        
        
        # CREATE PLAYER RESULTS
        for player_result in request_data['playerResults']:
            player_key = ndb.Key(Player, player_result['player_id'])
            
            # Create Player result
            player_result_key = PlayerResult(
                player = player_key,
                game = game_key,
                is_winner = player_result['is_winner'],
                score = player_result['score'],
                team = player_result['team'],
                civilization = player_result['civilization'],
            ).put()
            
#             # Create Player result stats
#             last_player_result_stats = PlayerResultStats._last_stats(player_result_key)
#             if last_player_result_stats: # Might be first game
#                 rating = next_rating_for_player(last_player_result_stats.rating, player_result['is_winner'])
#             else:
#                 rating = next_rating_for_player(PLAYER_RATING_START_VALUE, player_result['is_winner'])
#             
#             new_stats = PlayerResultStats(
#                 player_result = player_result_key,
#                 rating = rating
#             ).put()
#             
#             # Update previous/last player result stats setting the new player result stats as the next_stats
#             if last_player_result_stats:
#                 last_player_result_stats.next_stats = new_stats
#                 last_player_result_stats.put()
        
        
        self.abort(500) # Just so data doesnt have to be retyped in at gui
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Game saved"}))

def next_rating_for_player(last_stats_rating, is_winner):
    if is_winner == True:
        return last_stats_rating + 20
    else:
        return last_stats_rating - 20

class GameHandler(webapp2.RequestHandler):
    def get(self, game_id):
        logging.info("Returning data for game_id: %s", game_id)

        self.response.headers['Content-Type'] = 'application/json'
        obj = {'game_id': game_id, 'game_type': game_id} #kun for testdata

        self.response.out.write(json.dumps(obj))

    def put(self, gameId):
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("PUT (Update) received with data: " + self.request.body)


app = webapp2.WSGIApplication([
    (r'/api/games/', GamesHandler),
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