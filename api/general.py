#!/usr/bin/env python

import webapp2
import json
import logging
from google.appengine.ext import ndb
from models import Player
import math, random, copy

class SetupGameHandler(webapp2.RequestHandler):
    def post(self):
        request_data = json.loads(self.request.body)

        player_ids = request_data['players'] #[pl.key.id() for pl in Player.query().fetch()] # Should be replaced with reading from http post
        players = []
        for player_id in player_ids:
            player = ndb.Key(Player, int(player_id)).get()
            players.append({'id': player.key.id(), 'nick': player.nick, 'rating': player.rating()})
        logging.info(players)
        
        algorithm = request_data['algorithm'] # "Best random" # Should be replaced with reading from http post
        
        if algorithm == "Random":
            setup_data = _random_setup(players)
        elif algorithm == "Autobalance":
            setup_data = _random_setup_best_attempt(players, 50)

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(setup_data))

def _random_setup_best_attempt(players, attempts):
    best_setup = None
    for _ in range(attempts):
        potential_setup = _random_setup(players)
        if best_setup == None:
            best_setup = potential_setup
        elif potential_setup['total_rating_dif'] < best_setup['total_rating_dif']:
            best_setup = potential_setup
    return best_setup

def _random_setup(players_in):
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
        game = _random_team_split(game_players)
        total_rating_dif += game['rating_dif']
        games.append(game)
    
    return {'total_rating_dif': total_rating_dif, 'games': games}
            
def _random_team_split(players):
    teams_setup = {'rating_dif': None, 'teams': [[], []]}
    for i in range(len(players)):
        team_index = i % 2
        teams_setup['teams'][team_index].append(players[i])
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