#!/usr/bin/env python

import webapp2
import json
import logging
from models import PlayerResult, Player


class GlobalStatsHandler(webapp2.RequestHandler):
    def get(self):
        """
        No caching is used for GlobalStats, as a need has not been discovered. Performance has been good.
        If otherwise is experienced then we need to consider saving the global stats.
        """
        players = Player.query().fetch()

        teammate_fits = []
        civ_fits = []
        longest_winning_streak_number = 0
        longest_winning_streak_player = None
        longest_losing_streak_number = 0
        longest_losing_streak_player = None

        for player in players:
            player.calc_and_update_stats_if_needed()
            # Teammate fits
            if player.stats_teammate_fit:
                for teammate_fit in player.stats_teammate_fit:
                    if not self._does_fits_list_have_with_teammate(teammate_fits, player.key.id(), teammate_fit['teammate']['id']):
                        teammate_fit['player'] = {'id': player.key.id(), 'nick': player.nick}
                        teammate_fits.append(teammate_fit)
            # Civilization fits
            if player.stats_civ_fit:
                for civ_fit in player.stats_civ_fit:
                    civ_fit['player'] = {'id': player.key.id(), 'nick': player.nick}
                    civ_fits.append(civ_fit)
            # Streaks
            if player.stats_longest_winning_streak > longest_winning_streak_number:
                longest_winning_streak_number = player.stats_longest_winning_streak
                longest_winning_streak_player = player
            if player.stats_longest_losing_streak > longest_losing_streak_number:
                longest_losing_streak_number = player.stats_longest_losing_streak
                longest_losing_streak_player = player

        # Highest/Lowest rating achieved
        highest_rating_result = PlayerResult.query().order(-PlayerResult.stats_rating).get()
        lowest_rating_result = PlayerResult.query().order(PlayerResult.stats_rating).get()

        data = {
            'teammate_fits': teammate_fits,
            'civ_fits': civ_fits,
            'longest_winning_streak': {
                'number': longest_winning_streak_number,
                'player': {
                    'id': longest_winning_streak_player.key.id(),
                    'nick': longest_winning_streak_player.nick
                }
            },
            'longest_losing_streak': {
                'number': longest_losing_streak_number,
                'player': {
                    'id': longest_losing_streak_player.key.id(),
                    'nick': longest_losing_streak_player.nick
                }
            },
            'highest_rating_achieved': {
                'number': highest_rating_result.stats_rating,
                'player': {
                    'id': highest_rating_result.player.id(),
                    'nick': highest_rating_result.player.get().nick
                }
            },
            'lowest_rating_achieved': {
                'number': lowest_rating_result.stats_rating,
                'player': {
                    'id': lowest_rating_result.player.id(),
                    'nick': lowest_rating_result.player.get().nick
                }
            }
        }
        
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