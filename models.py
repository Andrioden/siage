from google.appengine.ext import ndb
import datetime
from collections import Counter
from config import PLAYER_RATING_START_VALUE
import logging
import operator

CIVILIZATIONS = ['Aztec', 'Britons', 'Byzantines', 'Celts', 'Chinese', 'Franks', 'Goths', 'Huns', 'Incas', 'Indians', 'Italians', 'Japanese', 'Koreans', 'Magyars', 'Mayans', 'Mongols', 'Persians', 'Saracens', 'Slavs', 'Spanish', 'Teutons', 'Turks', 'Vikings']

class Player(ndb.Model):
    nick = ndb.StringProperty(required=True)
    stats_average_score = ndb.IntegerProperty(default=None)
    stats_best_civ = ndb.StringProperty(choices=CIVILIZATIONS, default=None)
    stats_best_civ_wins = ndb.IntegerProperty(default=None)
    stats_worst_civ = ndb.StringProperty(choices=CIVILIZATIONS, default=None)
    stats_worst_civ_losses = ndb.IntegerProperty(default=None)
    def rating(self):
        """ To avoid hitting the db unneccessary the rating value is stored in memory.
        """
        if hasattr(self, "_current_rating_cached"):
            return self._current_rating_cached
        else:
            last_player_result = PlayerResult.get_last_result_for_player(self.key)
            self._current_rating_cached = 1000 if last_player_result == None else last_player_result.stats_rating
            return self._current_rating_cached
    def get_data_base(self):
        return {
            'id': self.key.id(), 
            'nick': self.nick, 
            'rating': self.rating(),
            'played': PlayerResult.query(PlayerResult.player==self.key).count(),
            'wins': PlayerResult.query(PlayerResult.player==self.key, PlayerResult.is_winner==True).count(),
        }
    def get_data_full(self):
        """ Gets (and calcs if neccessary) all statistics, also updates it to db if any 
        stats was calculated
        
        """
        data = self.get_data_base()
        
        self.calc_and_put_stats_if_needed()
        stats_data = {
            'average_score': self.stats_average_score,
            'best_civ': {
                'name': self.stats_best_civ,
                'wins': self.stats_best_civ_wins
            },
            'worst_civ': {
                'name': self.stats_worst_civ,
                'losses': self.stats_worst_civ_losses
            }
        #     Most played civ
        #     Best team mate winchance
        #     Worst team mate winchance
        #     Best team mate avg score
        #     Worst team mate avg score
        #     Average score
        #     Best score - show game
        #     Worst score - show game
        }
        data.update(stats_data)
        return data
    def calc_and_put_stats_if_needed(self):
        if self.stats_average_score == None:
            self.calc_stats()
            self.put()
    def calc_stats(self):
        player_results = PlayerResult.query(PlayerResult.player == self.key).fetch()
        # Average score
        self.stats_average_score = sum([result.score for result in player_results]) / len(player_results)
        # Best civ stats
        civ_won_dict = {}
        for result in player_results:
            if result.is_winner:
                if not civ_won_dict.has_key(result.civilization):
                    civ_won_dict[result.civilization] = 0
                civ_won_dict[result.civilization] += 1
        if len(civ_won_dict) > 0:
            best_civ = max(civ_won_dict.iteritems(), key=operator.itemgetter(1))[0]
            self.stats_best_civ = best_civ
            self.stats_best_civ_wins = civ_won_dict[best_civ]
        # Worst civ stats
        civ_lost_dict = {}
        for result in player_results:
            if result.is_winner == False:
                if not civ_lost_dict.has_key(result.civilization):
                    civ_lost_dict[result.civilization] = 0
                civ_lost_dict[result.civilization] += 1
        if len(civ_lost_dict) > 0:
            worst_civ = max(civ_lost_dict.iteritems(), key=operator.itemgetter(1))[0]
            self.stats_worst_civ = worst_civ
            self.stats_worst_civ_losses = civ_lost_dict[worst_civ]
        # MOAR STATS using player_results
    def clear_stats(self):
        self.stats_average_score = None
        self.stats_best_civ = None
        self.stats_worst_civ = None
        self.put()


class Game(ndb.Model):
    # After finish values
    date = ndb.DateTimeProperty(required=False)
    duration_seconds = ndb.IntegerProperty(required=False)
    # Settings from lobby Game Settings
    game_type = ndb.StringProperty(required=False, choices=['Random Map', 'Turbo Random Map', 'Regicide', 'Death Match', 'Scenario', 'King of the Hill', 'Wonder Race', 'Defend the Wonder', 'Capture the Relic'])
    size = ndb.StringProperty(required=False, choices=['Tiny (2 player)', 'Small (3 player)', 'Medium (4 player)', 'Normal (6 player)', 'Large (8 player)', 'Giant', 'LudiKRIS'])
    difficulty = ndb.StringProperty(required=False, choices=['Easiest', 'Standard', 'Moderate', 'Hard', 'Hardest'])
    resources = ndb.StringProperty(required=False, choices=['Standard', 'Low', 'Medium', 'High'])
    population = ndb.IntegerProperty(required=False, choices=[25, 50, 75, 100, 125, 150, 175, 200, 300, 400, 500])
    game_speed = ndb.StringProperty(required=False, choices=['Slow', 'Normal', 'Fast'])
    reveal_map = ndb.StringProperty(required=False, choices=['Normal', 'Explored', 'All Visible'])
    starting_age = ndb.StringProperty(required=False, choices=['Standard','Dark Age', 'Feudual Age', 'Castle Age', 'Imperial Age', 'Post-Imperial Age'])
    treaty_length = ndb.IntegerProperty(required=False, choices=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 90])
    victory = ndb.StringProperty(required=False, choices=['Standad', 'Conquest', 'Time Limit', 'Score', 'Last Man Standing'])
    team_together = ndb.BooleanProperty(required=False)
    all_techs = ndb.BooleanProperty(required=False)
    # Settings from Objective screen ingame
    location = ndb.StringProperty(required=False, choices=['Arabia', 'Archipelago', 'Arena', 'Baltic', 'Black Forest', 'Coastal', 'Continental', 'Crater Laker', 'Fortress', 'Ghost Lake', 'Gold Rush', 'Highland', 'Islands', 'Mediterranean', 'Migration', 'Mongolia', 'Nomad', 'Oasis', 'Rivers', 'Salt Marsh', 'Scandinavia', 'Team Islands', 'Yucatan', 'Acropolis', 'Budapest', 'Cenotes', 'City of Lakes', 'Golden Pit', 'Hideout', 'Hill Fort', 'Lombardia', 'Steppe', 'Valley', 'MegaRandom', 'Hamburger'])
    # Special settings
    trebuchet_allowed = ndb.BooleanProperty(required=False)
    def get_data(self):
        player_results_data = [res.get_data() for res in PlayerResult.query(PlayerResult.game==self.key)]
        return {
            'id': self.key.id(),
            'title': "%s %s" % (self.game_type, self.location),
            'team_format': self._player_results_to_game_format(player_results_data),
            'date': self.date.strftime("%Y-%m-%d"),
            'date_epoch': int((self.date - datetime.datetime(1970,1,1)).total_seconds()),
            'duration_seconds': self.duration_seconds,
            'game_type': self.game_type,
            'size': self.size,
            'difficulty': self.difficulty,
            'resources': self.resources,
            'population': self.population,
            'game_speed': self.game_speed,
            'reveal_map': self.reveal_map,
            'starting_age': self.starting_age,
            'treaty_length': self.treaty_length,
            'victory': self.victory,
            'team_together': self.team_together,
            'all_techs': self.all_techs,
            'location': self.location,
            'trebuchet_allowed': self.trebuchet_allowed,
            'player_results': player_results_data
        }
    def _player_results_to_game_format(self, player_results):
        teams = [player_data['team'] for player_data in player_results]
        counted_teams = Counter(teams)
        game_format = ""
        # First add people with teams, sorted by the most common
        for key, value in counted_teams.most_common():
            if key == None: # People without teams is dealth with afterwards so v1v1.. is at the end
                pass
            else:
                game_format += "%sv" % value
        # Then add the teamless as v1v1v1v1.. etc
        for _ in range(counted_teams[None]):
            game_format += "1v"
        # Return all but extra v
        return game_format[:-1]
    @classmethod
    def _settings_data(cls):
        return {
            'game_types': list(cls.game_type._choices),
            'sizes': list(cls.size._choices),
            'difficulties': list(cls.difficulty._choices),
            'resources': list(cls.resources._choices),
            'populations': list(cls.population._choices),
            'game_speeds': list(cls.game_speed._choices),
            'reveal_map': list(cls.reveal_map._choices),
            'starting_ages': list(cls.starting_age._choices),
            'treaty_lengths': list(cls.treaty_length._choices),
            'victories': list(cls.victory._choices),
            'locations': list(cls.location._choices)
        }

class PlayerResult(ndb.Model):
    player = ndb.KeyProperty(kind=Player, required=True)
    game = ndb.KeyProperty(kind=Game, required=True)
    game_date = ndb.DateTimeProperty(required=False) # This is doublestorage of info ues, but its to simplify queries
    is_winner = ndb.BooleanProperty(default=False)
    is_host = ndb.BooleanProperty(default=False)
    score = ndb.IntegerProperty(required=True)
    team = ndb.IntegerProperty(choices=[1,2,3,4])
    civilization = ndb.StringProperty(required=True, choices=CIVILIZATIONS)
    stats_rating = ndb.IntegerProperty(required=True)
    @classmethod
    def _settings_data(cls):
        return {
            'teams': list(cls.team._choices),
            'civilizations': list(cls.civilization._choices)
        }
    @classmethod
    def get_last_result_for_player(cls, player_key):
        return PlayerResult.query(PlayerResult.player == player_key).order(-PlayerResult.game_date).get()
    def get_previous_result(self):
        return PlayerResult.query(PlayerResult.player == self.player, PlayerResult.game_date < self.game_date).get()
    def get_data(self):
        player_entity = self.player.get()
        return{
            'player': {'id': player_entity.key.id(), 'nick': player_entity.nick},
            'game': self.game.id(),
            'is_winner': self.is_winner,
            'is_host': self.is_host,
            'score': self.score,
            'team': self.team,
            'civilization': self.civilization,
            'stats_rating': self.stats_rating,
            'rating_earned': self.rating_earned()
        }
    def rating_earned(self):
        previous_result = self.get_previous_result()
        if previous_result:
            return self.stats_rating - previous_result.stats_rating
        else:
            return self.stats_rating - PLAYER_RATING_START_VALUE