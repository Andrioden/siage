#!/usr/bin/env python

import webapp2
import json
import logging
from google.appengine.ext import ndb
from models import Player, Rule, CIVILIZATIONS
import math
import random
import copy
from google.appengine.api import users
from utils import *
from config import MAX_SETUP_GAME_ATTEMPTS


class SetupGameHandler(webapp2.RequestHandler):
    def post(self):
        # GET REQUEST DATA
        request_data = json.loads(self.request.body)
        algorithm = request_data['algorithm']
        player_inputs = request_data['players']
        max_game_rating_dif = request_data['max_game_rating_dif']
        attempts = min(request_data.get("attempts", 100), MAX_SETUP_GAME_ATTEMPTS)

        team_setup = "XvX"
        if "team_setup" in request_data:
            if request_data["team_setup"]:
                team_setup = request_data["team_setup"]
                if not self._validate_team_setup(len(player_inputs), team_setup):
                    return

        # BUILD GAME SETUP RESPONSE
        players = []
        for player_input in player_inputs:
            player = ndb.Key(Player, int(player_input['id'])).get()
            player.calc_and_update_stats_if_needed()
            score_per_min = player.stats_average_score_per_min if player.stats_average_score_per_min else 0
            players.append({'id': player.key.id(), 'nick': player.nick, 'rating': player_input['rating'], 'score_per_min': score_per_min})
        
        if algorithm == "RandomManyTeams":
            setup_data = self._random_setup(players, "random_team_setup")
        elif algorithm == "Random":
            setup_data = self._random_setup(players, team_setup)
        elif algorithm == "AutoBalance":
            setup_data = self._random_setup_best_attempt(players, attempts, team_setup, max_game_rating_dif)
        elif algorithm == "AutoBalanceSAMR":
            setup_data = self._random_setup_best_attempt_score_and_minirandomized_rating(players, attempts, team_setup, max_game_rating_dif)

        if setup_data is None:
            error(400, self.response, "ERROR_NO_SETUP_FOUND", "No setup found with the given settings within %s attempts. Please change settings." % MAX_SETUP_GAME_ATTEMPTS)
            return

        self._add_civilization_to_players(setup_data['games'])

        # RETURN RESPONSE
        set_json_response(self.response, setup_data)

    def _random_setup_best_attempt_score_and_minirandomized_rating(self, players, attempts, team_setup, max_game_rating_dif):
        setup_avg_score_per_min = sum([player['score_per_min'] for player in players])

        for player in players:
            percent_of_setup_avg = player['score_per_min'] / setup_avg_score_per_min
            skill_score_impact = 10 * (percent_of_setup_avg - 1)
            skill_randomness = random.randint(-5,5)
            skill_guess = player['rating'] + skill_score_impact + skill_randomness
            player['rating'] = int(skill_guess)

        return self._random_setup_best_attempt(players, attempts, team_setup, max_game_rating_dif)

    def _random_setup_best_attempt(self, players, attempts, team_setup, max_game_rating_dif):
        best_setup = None
        attempts_done = 0
        attempts_left = attempts
        while attempts_left >= 0:
            attempts_done += 1
            if attempts_done > MAX_SETUP_GAME_ATTEMPTS:
                break

            potential_setup = self._random_setup(players, team_setup, max_game_rating_dif)
            if potential_setup is None:
                continue

            if best_setup is None:
                best_setup = potential_setup
            elif potential_setup['total_rating_dif'] < best_setup['total_rating_dif']:
                best_setup = potential_setup
            attempts_left -= 1
        return best_setup

    def _random_setup(self, players_in, team_setup, max_game_rating_dif=9999):
        players = copy.deepcopy(players_in)
        # 1. Create the amount of games needed for the amount of players
        game_count = int(math.ceil(len(players) * 1.0 / 8))
        games_players = [[] for _ in range(game_count)] # Create a twidimensional array with games_players[game][player] format.

        # 2. Split the players into the different games randomly
        for i in range(len(players)):
            game_index = (i/2) % game_count
            random_player = players.pop(random.randint(0, len(players)-1))
            games_players[game_index].append(random_player)

        # 3. Find random or algorithm based team
        games = []
        total_rating_dif = 0
        for game_players in games_players:
            if team_setup == "random_team_setup":
                number_of_teams = random.randint(2, len(game_players))
                game = self._random_team_split_for_game(game_players, number_of_teams)
            elif team_setup == "XvX":
                game = self._random_team_split_for_game(game_players)
            else:
                game = self._random_team_split_for_game_using_predefined_setup(game_players, team_setup)

            if game['rating_dif'] > max_game_rating_dif:
                return None
            else:
                total_rating_dif += game['rating_dif']
                games.append(game)

        return {'total_rating_dif': total_rating_dif, 'games': games}

    def _random_team_split_for_game(self, players, number_of_teams=2):
        teams_setup = {
            'rating_dif': None,
            'teams': [{'rating': 0, 'players': []} for _ in range(number_of_teams)]
        }
        for i in range(len(players)):
            team_index = i % number_of_teams
            teams_setup['teams'][team_index]['rating'] += players[i]['rating']
            teams_setup['teams'][team_index]['players'].append(players[i])
        teams_setup['rating_dif'] = self._find_rating_dif(teams_setup['teams'])
        return teams_setup

    def _random_team_split_for_game_using_predefined_setup(self, players, setup):
        teams_setup = {
            'rating_dif': None,
            'teams': [{'rating': 0, 'size': int(team_size), 'players': []} for team_size in setup.split('v')]
        }

        for player in players:
            for team in teams_setup['teams']:
                if len(team['players']) < team['size']:
                    team['rating'] += player['rating']
                    team['players'].append(player)
                    break
        teams_setup['rating_dif'] = self._find_rating_dif(teams_setup['teams'])
        return teams_setup

    def _find_rating_dif(self, teams):
        max_total_rating = -1000
        min_total_rating = 99999
        for team in teams:
            total_rating = 0
            for player in team['players']:
                total_rating += player['rating']
            if total_rating > max_total_rating:
                max_total_rating = total_rating
            if total_rating < min_total_rating:
                min_total_rating = total_rating
        return max_total_rating - min_total_rating

    def _validate_team_setup(self, player_count, team_setup):
        team_setup_player_slots = sum([int(team_size) for team_size in team_setup.split('v')])
        if player_count > 8:
            error(400, self.response, "TEAM_SETUP_ERROR", "The algorithm does not support predefined team setup with more than 8 players. You tried with %s" % player_count)
            return False
        elif not player_count == team_setup_player_slots:
            error(400, self.response, "TEAM_SETUP_ERROR", "The amount of players (%s) do not match the team setup player slots (%s)" % (player_count, team_setup_player_slots))
            return False
        else:
            return True

    def _add_civilization_to_players(self, games):
        for game in games:
            for team in game['teams']:
                for player in team['players']:
                    player['civ'] = random.choice(CIVILIZATIONS)


class ClaimPlayerHandler(webapp2.RequestHandler):
    def get(self, player_id):
        player = Player.get_by_id(int(player_id))
        user = users.get_current_user()
        
        if player.userid:
            error(400, self.response, "PLAYER_CLAIMED", "The player %s has already been claimed by %s" % (player.nick, player.userid))
        else:
            if user:
                previously_claimed_player = Player.query(Player.userid == user.user_id()).get()
                if previously_claimed_player:
                    error(400, self.response, "CAN_ONLY_CLAIM_ONE_PLAYER", "The logged inn user has already claimed player %s" % previously_claimed_player.nick)
                else:
                    player.userid = user.user_id()
                    player.put()
                    return webapp2.redirect("/players/" + player.nick)
            else:
                error(400, self.response, "NOT_LOGGED_INN", "The visiting user is not logged inn.")



app = webapp2.WSGIApplication([
    (r'/api/actions/setupgame/', SetupGameHandler),
    (r'/api/actions/claimplayer/(\d+)', ClaimPlayerHandler),
], debug=True)