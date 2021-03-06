#!/usr/bin/env python

import webapp2
import json
import logging
from models import Game, Player, PlayerResult, Rule, CivilizationStats
from datetime import datetime
from google.appengine.ext import ndb
from rating import RatingCalculator, trigger_rating_decay_for_game
from api.utils import *


class GamesHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET GAMELIST --------- """
        max_rows = self.request.get('max')
        player_id = self.request.get('player_id')
        data_detail = self.request.get('data_detail', "simple")
        
        # First build base data in a common structure common for all api input combinations
        query = None
        if player_id:
            query = PlayerResult.query(PlayerResult.player == ndb.Key(Player, int(player_id))).order(-PlayerResult.game_date)
        else:
            query = Game.query().order(-Game.date)
        
        # Fetch with max_rows if present
        if max_rows.isdigit():
            if int(max_rows) > 0:
                data = query.fetch(limit = int(max_rows))
            else:
                data = query.fetch()
        else:
            data = query.fetch()
        
        # get data according to if its for a specific player or not
        if player_id:
            game_keys = [player_result.game for player_result in data]
            games_data = [game.get_data(data_detail) for game in ndb.get_multi(game_keys)]
            player = ndb.Key(Player, int(player_id)).get()
            player_rating_decay = player.rating_decay
            self._expand_game_data_with_player_result_data(games_data, data, player_rating_decay)
        else:
            games_data = [game.get_data(data_detail) for game in data]
        
        # RETURN RESPONSE
        set_json_response(self.response, games_data)

    def _expand_game_data_with_player_result_data(self, games_data, player_results, rating_decay):
        # Set stats rating from the player_results object
        for game in games_data:
            for res in player_results:
                if res.game.id() == game['id']:
                    game['is_winner'] = res.is_winner
                    game['stats_rating'] = res.stats_rating + rating_decay

    def post(self):
        """ --------- CREATE GAME --------- """
        request_data = json.loads(self.request.body)

        # VALIDATING
        if not validate_request_data(self.response, request_data, ['location', 'size']):
            return
        if not request_data['duration_seconds']: # Has to be validated like this because input is 0
            error(400, self.response, "VALIDATION_ERROR_NO_DURATION", "Missing input: Duration.")
            return
        if not self._validate_no_empty_player_results(request_data['playerResults']):
            return
        if not validate_authenticated(self.response):
            return

        # CREATE GAME OBJECT
        game_date = datetime.fromtimestamp(request_data['date_epoch'])

        rule_id = request_data.get('rule', None)
        if rule_id:
            rule_key = ndb.Key(Rule, int(rule_id))
        else:
            rule_key = None

        game = Game(
            rule = rule_key,
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
        ).put().get()

        # CREATE PLAYER RESULTS
        rc = RatingCalculator()
        rc.add_player_results_from_dict(request_data['playerResults'])
        new_ratings = rc.calc_and_get_new_rating_dict()

        player_results = []
        for player_result in request_data['playerResults']:
            player_key = ndb.Key(Player, int(player_result['player_id']))
            
            player_result_obj = PlayerResult(
                player = player_key,
                game = game.key,
                game_date = game_date,
                is_winner = player_result['is_winner'],
                score = player_result['score'],
                team = player_result['team'],
                civilization = player_result['civilization'],
                stats_rating = new_ratings[player_key.id()]
            ).put().get()

            player_results.append(player_result_obj)

        trigger_rating_decay_for_game(game.date, player_results)

        self._clear_all_player_stats()
        ndb.delete_multi(CivilizationStats.query().fetch(keys_only=True))

        # RETURN RESPONSE
        set_json_response(self.response, {'response': "success", 'game_id': game.key.id()})

    def _validate_no_empty_player_results(self, player_results):
        for player_result in player_results:
            if player_result['player_id'] is None or not player_result['player_id']:
                error(400, self.response, "VALIDATION_ERROR_EMPTY_PLAYER_RESULTS", "Player Results contain items without a valid player id.")
                return False
        return True

    def _clear_all_player_stats(self):
        for player in Player.query():
            player.clear_stats()


class GameHandler(webapp2.RequestHandler):
    def get(self, game_id):
        """ --------- GET SINGLE GAME --------- """
        data_detail = self.request.get('data_detail', "simple")
        
        # BUILD DATA
        game = Game.get_by_id(int(game_id))

        # RETURN RESPONSE
        if game:
            set_json_response(self.response, game.get_data(data_detail))
        else:
            error(404, self.response, "GAME_NOT_FOUND", "Game with ID '%s' not found" % game_id)


app = webapp2.WSGIApplication([
    (r'/api/games/', GamesHandler),
    (r'/api/games/(\d+)', GameHandler),
], debug=True)