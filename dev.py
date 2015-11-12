#!/usr/bin/env python

'''
A module used for development
'''

import random
from datetime import datetime, timedelta
from models import *
from rating import recalculate_ratings

def add_test_data_all():
    add_test_data_players()
    add_test_data_games(20)

def add_test_data_players():
    print "Creating players..."
    Player(nick = "Andriod").put()
    Player(nick = "Dust").put()
    Player(nick = "Kartoffel").put()
    Player(nick = "Ninja").put()
    Player(nick = "Knsnsns").put()
    Player(nick = "Lolmannen").put()
    Player(nick = "Kaku").put()
    Player(nick = "Gerrard").put()
    Player(nick = "Torres").put()
    print "Creating players DONE"

def add_test_data_games(number_of_games):
    for i in range(number_of_games):
        add_test_data_randomized_game(datetime.now() - timedelta(days=number_of_games-i))
    recalculate_ratings()
    print "Creating games data DONE"


def add_test_data_randomized_game(game_date):
    game_key = Game(
        # After finish values
        date = game_date,
        duration_seconds = random.randint(40,300)*60,
        # Settings from lobby Game Settings
        game_type = random.choice(list(Game.game_type._choices)),
        size = random.choice(list(Game.size._choices)),
        difficulty = random.choice(list(Game.difficulty._choices)),
        resources = random.choice(list(Game.resources._choices)),
        population = random.choice(list(Game.population._choices)),
        game_speed = random.choice(list(Game.game_speed._choices)),
        reveal_map = random.choice(list(Game.reveal_map._choices)),
        starting_age = random.choice(list(Game.starting_age._choices)),
        treaty_length = random.choice(list(Game.treaty_length._choices)),
        victory = random.choice(list(Game.victory._choices)),
        team_together = True,
        all_techs = True,
        # Settings from Objective screen ingame
        location = random.choice(list(Game.location._choices)),
        # Special settings
        trebuchet_allowed = False
    ).put()

    players = Player.query().fetch()
    random.shuffle(players)

    total_players_this_game = random.randint(2,8)
    for i in range(total_players_this_game):
        PlayerResult(
            player = players[i].key,
            game = game_key,
            game_date = game_date,
            is_winner = True if (i < total_players_this_game / 2) else False,
            score = random.randint(2000,40000),
            team = 1 if (i < total_players_this_game / 2) else 2,
            civilization = random.choice(list(CIVILIZATIONS)),
            stats_rating = 0
        ).put()