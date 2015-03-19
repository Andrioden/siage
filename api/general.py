#!/usr/bin/env python

import webapp2
import json
import logging
from google.appengine.ext import ndb
from models import Player
import math, random

class SetupGameHandler(webapp2.RequestHandler):
    def post(self):
        player_ids = [4537134732017664, 4572868859920384, 4751539499433984, 5021194726146048, 5021194726146048, 5021194726146048, 5021194726146048, 5021194726146048, 5021194726146048]
#         logging.info(self.request.POST)
#         player_ids = self.request.POST.get('players')
#         logging.info(player_ids)
        players = [ndb.Key(Player, int(player_id)).get() for player_id in player_ids]
        logging.info(players)

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(_random_setup(players)))

def _random_setup(players):
    # 1. Create the games_players
    game_count = int(math.ceil(len(players) * 1.0 / 8))
    games_players = [[] for _ in range(game_count)] # Create a twidimensional array with games_players[game][player] format.
            
    # 2. Split the players into the different games_players randomly
    for i in range(len(players)):
        game_index = i % game_count
        random_player = players.pop(random.randint(0, len(players)-1))
        games_players[game_index].append(random_player)
    logging.info(games_players)
    
    # 3. Find random or algorithm based team
    games = []
    total_rating_dif = 0
    for game_players in games_players:
        game = _random_team_split(game_players)
        total_rating_dif += game['rating_dif']
        games.append(game)
    
    return {'total_rating_dif': total_rating_dif, 'games': games}
            
def _random_team_split(players):
    teams_setup = {'rating_dif': None, 'teams': [[], []]}
    for i in range(len(players)):
        team_index = i % 2
        teams_setup['teams'][team_index].append({'id': players[i].key.id(), 'nick': players[i].nick, 'rating': players[i].rating()})
    teams_setup['rating_dif'] = _find_rating_dif(teams_setup['teams'])
    return teams_setup

def _find_rating_dif(teams):
    max_total_rating = -1000
    min_total_rating = 99999
    for team in teams:
        total_rating = 0
        for player in team:
            total_rating += player['rating']
        if total_rating > max_total_rating:
            max_total_rating = total_rating
        if total_rating < min_total_rating:
            min_total_rating = total_rating
    return max_total_rating - min_total_rating

app = webapp2.WSGIApplication([
    (r'/api/setupgame/', SetupGameHandler),
], debug=True)