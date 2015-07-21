#!/usr/bin/env python

import webapp2
import json
from google.appengine.ext import ndb
from rating import recalculate_ratings
from models import Player, CivilizationStats
from api.utils import validate_logged_in_admin
import logging


class ReCalcRatingHandler(webapp2.RequestHandler):
    def post(self):

        if not validate_logged_in_admin(self.response):
            return

        recalculate_ratings()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Ratings recalculated"}))


class CleanDBHandler(webapp2.RequestHandler):
    def post(self):
        """ This admin function will contain all historic and current clean up method.
        Please uncomment them when they are run on prod

        """

        if not validate_logged_in_admin(self.response):
            return

        # logging.info("----- 01.04.2015 - PlayerResult: removing next_player_result  ------")
        # for res in PlayerResult.query():
        #     if 'next_player_result' in res._properties:
        #         del res._properties['next_player_result']
        #     res.game_date = res.game.get().date
        #     res.put()
        #
        # logging.info("----- 01.04.2015 - Player: removing some stats best/worst properties  ------")
        # for player in Player.query():
        #     self._delete_property(player, 'stats_best_civ')
        #     self._delete_property(player, 'stats_best_civ_wins')
        #     self._delete_property(player, 'stats_worst_civ')
        #     self._delete_property(player, 'stats_worst_civ_losses')
        #     self._delete_property(player, 'stats_civ_most_wins_name')
        #     self._delete_property(player, 'stats_civ_most_wins_count')
        #     self._delete_property(player, 'stats_civ_most_losses_name')
        #     self._delete_property(player, 'stats_civ_most_losses_count')
        #     player.put()

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
        ndb.delete_multi(CivilizationStats.query().fetch(keys_only=True))

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Player statistics have been cleared"}))


class AdjustRatingHandler(webapp2.RequestHandler):
    def post(self):

        request_data = json.loads(self.request.body)
        player_id = request_data['player_id']
        new_rating_adjustment = request_data['new_rating_adjustment']

        player = Player.get_by_id(int(player_id))
        player.set_new_rating_adjustment(new_rating_adjustment)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "%s now has an rating adjustment at %s. Remember to recalculate ratings if player have been part of games." % (player.nick, new_rating_adjustment)}))

class ResetRatingAdjustment(webapp2.RequestHandler):
    def post(self):

        for player in Player.query().fetch():
            player.rating_adjustment = 0
            player.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "Rating adjustment reset. Remember to recalculate ratings if player have been part of games."}))

app = webapp2.WSGIApplication([
    (r'/api/actions/admin/recalcrating/', ReCalcRatingHandler),
    (r'/api/actions/admin/cleandb/', CleanDBHandler),
    (r'/api/actions/admin/clearstats/', ClearStatsHandler),
    (r'/api/actions/admin/adjustrating/', AdjustRatingHandler),
    (r'/api/actions/admin/resetratingadjustment/', ResetRatingAdjustment),
], debug=True)