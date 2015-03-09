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
            # After finish values
            #date = request_data['game_date']), 
            duration_seconds = request_data['duration_minutes']*60,
            # Settings from lobby Game Settings
            game_type = request_data['game_type'],
            size = request_data['size'],
            difficulty = request_data['difficulty'],
            resources = request_data['resources'],
            population = request_data['population'],
            game_speed = request_data['game_speed'],
            reveal_map = str(request_data['reveal_map']),
            starting_age = request_data['starting_age'],
            #treaty_length = request_data['treaty_length'],
            victory = request_data['victory'],
            team_together = request_data['team_together'] == "true",
            all_techs = request_data['all_techs'] == "true",
            # Settings from Objective screen ingame
            map_type = request_data['map_type'],
            # Special settings
            trebuchet_allowed = request_data['trebuchet_allowed'] == "true"
        ).put()
        
        
        # CREATE PLAYER RESULTS
        for player_result in request_data['playerResults']:
            player_key = ndb.Key(Player, int(player_result['player_id']))
            
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
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Game saved"}))

def next_rating_for_player(last_stats_rating, is_winner):
    if is_winner == True:
        return last_stats_rating + 20
    else:
        return last_stats_rating - 20

class GameHandler(webapp2.RequestHandler):
    def get(self, game_id):
        """ --------- GET SINGLE GAME --------- """
        logging.info("Returning data for game_id: %s", game_id)

        # BUILD DATA
        game = Game.get_by_id(int(game_id))

        # RETURN RESPONSE
        if game:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(game.get_data()))
        else:
            self.response.out.write(json.dumps({'error': "GAME_NOT_FOUND"}))

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