#!/usr/bin/env python

import webapp2
import json
import logging
from models import PlayerResult, Player


class GlobalStatsHandler(webapp2.RequestHandler):
    def get(self):
        players = Player.query().fetch()

        teammate_fits = []
        civ_fits = []
        for player in players:
            player.calc_and_update_stats_if_needed()
            if player.stats_teammate_fit:
                for teammate_fit in player.stats_teammate_fit:
                    if not self._does_fits_list_have_with_teammate(teammate_fits, player.key.id(), teammate_fit['teammate']['id']):
                        teammate_fit['player'] = {'id': player.key.id(), 'nick': player.nick}
                        teammate_fits.append(teammate_fit)
            if player.stats_civ_fit:
                for civ_fit in player.stats_civ_fit:
                    civ_fit['player'] = {'id': player.key.id(), 'nick': player.nick}
                    civ_fits.append(civ_fit)

        data = {'teammate_fits': teammate_fits, 'civ_fits': civ_fits}
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))

    def _does_fits_list_have_with_teammate(self, teammate_fits, player1_id, player2_id):
        for teammate_fit in teammate_fits:
            if teammate_fit['teammate']['id'] == player1_id and teammate_fit['player']['id'] == player2_id:
                return True
            elif teammate_fit['teammate']['id'] == player2_id and teammate_fit['player']['id'] == player1_id:
                return True
        return False

app = webapp2.WSGIApplication([
    (r'/api/globalstats/', GlobalStatsHandler),
], debug=True)