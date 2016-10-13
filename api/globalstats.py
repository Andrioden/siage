#!/usr/bin/env python

import webapp2
import logging
import datetime
from models import PlayerResult, Player, Game
from utils import *


class GlobalStatsHandler(webapp2.RequestHandler):
    def get(self):
        """
        No caching is used for GlobalStats, as a need has not been discovered. Performance has been good.
        If otherwise is experienced then we need to consider saving the global stats.
        """
        players = Player.query().fetch()

        teammate_fits = []
        enemy_fits = []
        civ_fits = []
        longest_winning_streak_number = 0
        longest_winning_streak_player = None
        longest_losing_streak_number = 0
        longest_losing_streak_player = None
        games_without_treb_and_cannon_won = 0
        games_without_treb_and_cannon_total = 0

        for player in players:
            player.calc_and_update_stats_if_needed()
            # Teammate fits
            if player.stats_teammate_fit:
                for teammate_fit in player.stats_teammate_fit:
                    if not self._does_fits_list_have_with_teammate(teammate_fits, player.key.id(), teammate_fit['teammate']['id']):
                        teammate_fit['player'] = {'id': player.key.id(), 'nick': player.nick}
                        teammate_fits.append(teammate_fit)
            # Enemy fits
            if player.stats_enemy_fit:
                for enemy_fit in player.stats_enemy_fit:
                    enemy_fit['player'] = {'id': player.key.id(), 'nick': player.nick}
                    enemy_fits.append(enemy_fit)
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
            # Without treb or bomb cannon
            games_without_treb_and_cannon_won += player.stats_games_without_treb_and_cannon_won
            games_without_treb_and_cannon_total += player.stats_games_without_treb_and_cannon_total

        longest_game = Game.query().order(-Game.duration_seconds).get()
        shortest_game = Game.query().order(Game.duration_seconds).get()

        data = {
            'teammate_fits': teammate_fits,
            'enemy_fits': enemy_fits,
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
            'longest_game': {
                'duration_seconds': longest_game.duration_seconds,
                'id': longest_game.key.id()
            },
            'shortest_game': {
                'duration_seconds': shortest_game.duration_seconds,
                'id': shortest_game.key.id()
            },
            'games_without_treb_and_cannon_win_chance': games_without_treb_and_cannon_won * 100 / games_without_treb_and_cannon_total
        }

        set_json_response(self.response, data)

    def _does_fits_list_have_with_teammate(self, teammate_fits, player1_id, player2_id):
        for teammate_fit in teammate_fits:
            if teammate_fit['teammate']['id'] == player1_id and teammate_fit['player']['id'] == player2_id:
                return True
            elif teammate_fit['teammate']['id'] == player2_id and teammate_fit['player']['id'] == player1_id:
                return True
        return False


class GlobalStatsActivityHandler(webapp2.RequestHandler):
    def get(self):
        activity = []

        start_date_of_current_session = PlayerResult.query().order(PlayerResult.game_date).get().game_date
        players_current_session= []

        for player_res in PlayerResult.query().order(PlayerResult.game_date).fetch():
            if (player_res.game_date - start_date_of_current_session).total_seconds() > 15*60*60:
                activity.append({'date_epoch': date_to_epoch(start_date_of_current_session), 'player_count': len(players_current_session)})
                start_date_of_current_session = player_res.game_date
                players_current_session = []

            if player_res.player not in players_current_session:
                players_current_session.append(player_res.player)

        activity.append({'date_epoch': date_to_epoch(start_date_of_current_session), 'player_count': len(players_current_session)})
        logging.info("NEW SESSION with date %s" % start_date_of_current_session)

        set_json_response(self.response, activity)


app = webapp2.WSGIApplication([
    (r'/api/globalstats/base/', GlobalStatsHandler),
    (r'/api/globalstats/activity/', GlobalStatsActivityHandler),
], debug=True)