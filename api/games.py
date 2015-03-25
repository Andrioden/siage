#!/usr/bin/env python

import webapp2
import json
import logging
from models import Game, Player, PlayerResult
from datetime import datetime
from google.appengine.ext import ndb
from rating import RatingCalculator

class GamesHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET GAMELIST --------- """
        max_rows = self.request.get('max')
        player_id_or_nick = self.request.get('player_id')

        # BUILD DATA
        query = Game.query()

        if max_rows.isdigit():
            if int(max_rows) > 0:
                query = query.fetch(limit = int(max_rows))

        if player_id_or_nick:
            if player_id_or_nick.isdigit():
                query = query # TODO: Add player.id = player_id_or_nick
            else:
                query = query # TODO: Add player.nick = player_id_or_nick            
        
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
        self._validate_no_empty_player_results(request_data['playerResults'])

        # CREATE GAME OBJECT
        game_key = Game(
            # After finish values
            date = datetime.fromtimestamp(request_data['date_epoch']),
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
            
            last_player_result = PlayerResult._last_result(player_key) # Get previous player result before we insert a new one
            
            new_player_result_key = PlayerResult(
                player = player_key,
                game = game_key,
                is_winner = player_result['is_winner'],
                is_host = player_result['is_host'],
                score = player_result['score'],
                team = player_result['team'],
                civilization = player_result['civilization'],
                stats_rating = new_ratings[player_key.id()]
            ).put()

            # Update previous/last player result stats setting the new player result stats as the next_stats
            if last_player_result:
                last_player_result.next_player_result = new_player_result_key
                last_player_result.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Success!", 'game_id': game_key.id()}))

    def _validate_no_empty_player_results(self, player_results):
        for player_result in player_results:
            if player_result['player_id'] == None or not player_result['player_id'].isdigit():
                raise Exception("Validation Error: Player Results contain items without a valid player id.")

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
