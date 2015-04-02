#!/usr/bin/env python

import webapp2
from rating import recalculate_ratings
from models import PlayerResult, Player
import logging

class RecalcHandler(webapp2.RequestHandler):
    def get(self):
        recalculate_ratings()
        self.response.write("OK")
        
class CleanDBHandler(webapp2.RequestHandler):
    def get(self):
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
        self.response.write("OK")
    def _delete_property(self, obj, property_name):
        if property_name in obj._properties:
            del obj._properties[property_name]
            
class ClearStatsHandler(webapp2.RequestHandler):
    def get(self):
        for player in Player.query():
            player.clear_stats()
        self.response.write("OK")
        
app = webapp2.WSGIApplication([
    (r'/admin/recalc/', RecalcHandler),
    (r'/admin/cleandb/', CleanDBHandler),
    (r'/admin/clearstats/', ClearStatsHandler),
], debug=True)