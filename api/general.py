#!/usr/bin/env python

import webapp2
import json
import logging
from google.appengine.ext import ndb
from models import Player
import math, random, copy
from google.appengine.api import users
from utils import error_400

class SetupGameHandler(webapp2.RequestHandler):
    def post(self):
        request_data = json.loads(self.request.body)

        player_ids = request_data['players']
        players = []
        for player_id in player_ids:
            player = ndb.Key(Player, int(player_id)).get()
            player.calc_and_update_stats_if_needed()
            score_per_min = player.stats_average_score_per_min if player.stats_average_score_per_min else 0
            players.append({'id': player.key.id(), 'nick': player.nick, 'rating': player.rating(), 'score_per_min': score_per_min})
        logging.info(players)
        
        algorithm = request_data['algorithm']
        
        if algorithm == "TotallyRandom":
            setup_data = self._random_setup(players, True)
        elif algorithm == "Random":
            setup_data = self._random_setup(players)
        elif algorithm == "Autobalance":
            setup_data = self._random_setup_best_attempt(players, 50)
        elif algorithm == "AutobalanceSR":
            setup_data = self._random_setup_best_attempt_score_and_minirandomized_rating(players, 25)

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(setup_data))

    def _random_setup_best_attempt_score_and_minirandomized_rating(self, players, attempts):
        setup_avg_score_per_min = sum([player['score_per_min'] for player in players])

        for player in players:
            skill_guess = player['rating'] + random.randint(-5,5)
            percent_of_setup_avg = player['score_per_min'] / setup_avg_score_per_min
            score_skill_change = 10 * (percent_of_setup_avg - 1)
            skill_guess += score_skill_change
            player['rating'] = int(skill_guess)

        return self._random_setup_best_attempt(players, attempts)

    def _random_setup_best_attempt(self, players, attempts):
        best_setup = None
        for _ in range(attempts):
            potential_setup = self._random_setup(players)
            if best_setup == None:
                best_setup = potential_setup
            elif potential_setup['total_rating_dif'] < best_setup['total_rating_dif']:
                best_setup = potential_setup
        return best_setup

    def _random_setup(self, players_in, random_number_of_teams=False):
        players = copy.deepcopy(players_in)
        # 1. Create the games_players
        game_count = int(math.ceil(len(players) * 1.0 / 8))
        games_players = [[] for _ in range(game_count)] # Create a twidimensional array with games_players[game][player] format.

        # 2. Split the players into the different games_players randomly
        for i in range(len(players)):
            game_index = 0 if (i % (game_count*2)) <= 1 else 1
            random_player = players.pop(random.randint(0, len(players)-1))
            games_players[game_index].append(random_player)
        logging.info(games_players)

        # 3. Find random or algorithm based team
        games = []
        total_rating_dif = 0
        for game_players in games_players:
            if random_number_of_teams:
                number_of_teams = random.randint(2, len(game_players))
                game = self._random_team_split_for_game(game_players, number_of_teams)
            else:
                game = self._random_team_split_for_game(game_players)
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

class ClaimPlayerHandler(webapp2.RequestHandler):
    def get(self, player_id):
        player = Player.get_by_id(int(player_id))
        user = users.get_current_user()
        
        if player.userid:
            error_400(self.response, "PLAYER_CLAIMED", "The player %s has already been claimed by %s" % (player.nick, player.userid))
        else:
            if user:
                previously_claimed_player = Player.query(Player.userid == user.user_id()).get()
                if previously_claimed_player:
                    error_400(self.response, "CAN_ONLY_CLAIM_ONE_PLAYER", "The logged inn user has already claimed player %s" % previously_claimed_player.nick)
                else:
                    player.userid = user.user_id()
                    player.put()
                    self.response.headers['Content-Type'] = 'application/json'
                    self.response.out.write(json.dumps({'response': "OK"}))
            else:
                error_400(self.response, "NOT_LOGGED_INN", "The visiting user is not logged inn.")
        
app = webapp2.WSGIApplication([
    (r'/api/setupgame/', SetupGameHandler),
    (r'/api/claimplayer/(\d+)', ClaimPlayerHandler),
], debug=True)