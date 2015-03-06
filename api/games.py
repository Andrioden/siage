#!/usr/bin/env python

import webapp2
import json
import logging
from models import Game, Player, PlayerResult
from datetime import datetime
from google.appengine.ext import ndb

PLAYER_RATING_START_VALUE = 1000

class GamesHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET GAMELIST --------- """
        # BUILD DATA
        game_data = [game.get_data() for game in Game.query()]
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(game_data))

    #@ndb.transactional
    def post(self):
        """ --------- CREATE GAME --------- """
        request_data = json.loads(self.request.body)
        logging.info(request_data)
        
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
            
            last_player_result = PlayerResult._last_result(player_key)
            if last_player_result: # Might be first game
                rating = next_rating_for_player(last_player_result.stats_rating, player_result['is_winner'])
            else:
                rating = next_rating_for_player(PLAYER_RATING_START_VALUE, player_result['is_winner'])
                
            # Create PlayerResult
            new_player_result_key = PlayerResult(
                player = player_key,
                game = game_key,
                is_winner = player_result['is_winner'],
                score = player_result['score'],
                team = player_result['team'],
                civilization = player_result['civilization'],
                stats_rating = rating
            ).put()
            
            # Update previous/last player result stats setting the new player result stats as the next_stats
            if last_player_result:
                last_player_result.next_player_result = new_player_result_key
                last_player_result.put()
        
#         self.abort(500) # Just so data doesnt have to be retyped in at gui
        
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