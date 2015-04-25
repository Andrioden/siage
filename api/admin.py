#!/usr/bin/env python

import webapp2
import json
from rating import recalculate_ratings
from models import PlayerResult, Player
from api.utils import validate_logged_in_admin
import logging


class RecalcHandler(webapp2.RequestHandler):
    def post(self):

        if not validate_logged_in_admin(self.response):
            return

        recalculate_ratings()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Ratings recalculated"}))


class CleanDBHandler(webapp2.RequestHandler):
    def post(self):

        if not validate_logged_in_admin(self.response):
            return

        """ This admin function will contain all historic and current clean up method.
        Please uncomment them when they are run on prod

        """
        logging.info("----- 01.04.2015 - PlayerResult: removing next_player_result  ------")
        for res in PlayerResult.query():
            if 'next_player_result' in res._properties:
                del res._properties['next_player_result']
            res.game_date = res.game.get().date
            res.put()

        logging.info("----- 01.04.2015 - Player: removing some stats best/worst properties  ------")
        for player in Player.query():
            self._delete_property(player, 'stats_best_civ')
            self._delete_property(player, 'stats_best_civ_wins')
            self._delete_property(player, 'stats_worst_civ')
            self._delete_property(player, 'stats_worst_civ_losses')
            self._delete_property(player, 'stats_civ_most_wins_name')
            self._delete_property(player, 'stats_civ_most_wins_count')
            self._delete_property(player, 'stats_civ_most_losses_name')
            self._delete_property(player, 'stats_civ_most_losses_count')
            player.put()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "The database has been cleaned"}))

    def _delete_property(self, obj, property_name):
        if property_name in obj._properties:
            del obj._properties[property_name]


class ClearStatsHandler(webapp2.RequestHandler):
    def post(self):

        if not validate_logged_in_admin(self.response):
            return

        for player in Player.query():
            player.clear_stats()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Player statistics have been cleared"}))


class UnverifiedPlayersHandler(webapp2.RequestHandler):
    def get(self):

        if not validate_logged_in_admin(self.response):
            return

        # BUILD DATA
        unverified_players = []
        for player in Player.query():
            if not player.verified:
                unverified_players.append(player.get_data())

        # RETURN DATA
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(unverified_players))


app = webapp2.WSGIApplication([
    (r'/api/admin/recalc/', RecalcHandler),
    (r'/api/admin/cleandb/', CleanDBHandler),
    (r'/api/admin/clearstats/', ClearStatsHandler),
    (r'/api/admin/unverifiedplayers/', UnverifiedPlayersHandler),
], debug=True)