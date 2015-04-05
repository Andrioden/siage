#!/usr/bin/env python

import webapp2
import json
import logging
from models import Game, Player, PlayerResult
from datetime import datetime
from google.appengine.ext import ndb
from rating import RatingCalculator
from api.utils import error_400, validate_logged_inn


class GamesHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET GAMELIST --------- """
        max_rows = self.request.get('max')

        # BUILD DATA
        query = Game.query()

        if max_rows.isdigit():
            if int(max_rows) > 0:
                query = query.fetch(limit = int(max_rows))

        game_data = [game.get_data() for game in query]
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(game_data))

    #@ndb.transactional
    def post(self):
        """ --------- CREATE GAME --------- """
        request_data = json.loads(self.request.body)
        logging.info(request_data)

        # VALIDATING
        if not self._validate_no_empty_player_results(request_data['playerResults']):
            return
        if not validate_logged_inn(self.response):
            return
        # CREATE GAME OBJECT
        game_date = datetime.fromtimestamp(request_data['date_epoch'])
        
        game_key = Game(
            # After finish values
            date = game_date,
            duration_seconds = request_data['duration_seconds'],
            # Settings from lobby Game Settings
            game_type = request_data['game_type'],
            size = request_data['size'],
            difficulty = request_data['difficulty'],
            resources = request_data['resources'],
            population = request_data['population'],
            game_speed = request_data['game_speed'],
            reveal_map = str(request_data['reveal_map']),
            starting_age = request_data['starting_age'],
            treaty_length = request_data['treaty_length'],
            victory = request_data['victory'],
            team_together = request_data['team_together'],
            all_techs = request_data['all_techs'],
            # Settings from Objective screen ingame
            location = request_data['location'],
            # Special settings
            trebuchet_allowed = request_data['trebuchet_allowed']
        ).put()

        # CREATE PLAYER RESULTS
        rc = RatingCalculator()
        rc.add_player_results_from_dict(request_data['playerResults'])
        new_ratings = rc.calc_and_get_new_rating_dict()

        for player_result in request_data['playerResults']:
            player_key = ndb.Key(Player, int(player_result['player_id']))
            
            PlayerResult(
                player = player_key,
                game = game_key,
                game_date = game_date,
                is_winner = player_result['is_winner'],
                is_host = player_result['is_host'],
                score = player_result['score'],
                team = player_result['team'],
                civilization = player_result['civilization'],
                stats_rating = new_ratings[player_key.id()]
            ).put()
        
        self._clear_all_player_stats() 

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Success!", 'game_id': game_key.id()}))
    def _validate_no_empty_player_results(self, player_results):
        for player_result in player_results:
            if player_result['player_id'] == None or not player_result['player_id'].isdigit():
                error_400(self.response, "VALIDATION_ERROR_EMPTY_PLAYER_RESULTS", "Player Results contain items without a valid player id.")
                return False
        return True
    def _clear_all_player_stats(self):
        for player in Player.query():
            player.clear_stats()

class GameHandler(webapp2.RequestHandler):
    def get(self, game_id):
        """ --------- GET SINGLE GAME --------- """

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