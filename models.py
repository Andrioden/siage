from google.appengine.ext import ndb
from datetime import datetime, date, timedelta
from collections import Counter
from config import PLAYER_RATING_START_VALUE
import logging
import operator

CIVILIZATIONS = ['Aztec', 'Britons', 'Byzantines', 'Celts', 'Chinese', 'Franks', 'Goths', 'Huns', 'Incas', 'Indians', 'Italians', 'Japanese', 'Koreans', 'Magyars', 'Mayans', 'Mongols', 'Persians', 'Saracens', 'Slavs', 'Spanish', 'Teutons', 'Turks', 'Vikings', 'Berbers', 'Ethiopians', 'Malians', 'Portuguese']


class Player(ndb.Model):
    nick = ndb.StringProperty(required=True)
    userid = ndb.StringProperty(default=None)
    verified = ndb.BooleanProperty(default=False)
    rating_adjustment = ndb.IntegerProperty(default=0)
    active = ndb.BooleanProperty(default=True)
    stats_average_score = ndb.IntegerProperty(default=None)
    stats_best_score = ndb.IntegerProperty(default=None)
    stats_best_score_game = ndb.KeyProperty(kind='Game', default=None)
    stats_worst_score = ndb.IntegerProperty(default=None)
    stats_worst_score_game = ndb.KeyProperty(kind='Game', default=None)
    stats_average_score_per_min = ndb.FloatProperty(default=None)
    stats_best_score_per_min = ndb.FloatProperty(default=None)
    stats_best_score_per_min_game = ndb.KeyProperty(kind='Game', default=None)
    stats_percentage_topping_score = ndb.FloatProperty(default=None)
    stats_worst_score_per_min = ndb.FloatProperty(default=None)
    stats_worst_score_per_min_game = ndb.KeyProperty(kind='Game', default=None)
    stats_longest_winning_streak = ndb.IntegerProperty(default=None)
    stats_longest_losing_streak = ndb.IntegerProperty(default=None)
    """
    The teammate_fit is a list with data in the following format: {
        'teammate': {
            'id': X1,
            'nick': X2
        },
        'played': X3,
        'wins': X4
        'win_chance': X5,
        'points': X6
    }
    """
    stats_teammate_fit = ndb.PickleProperty(default=None)
    stats_enemy_fit = ndb.PickleProperty(default=None)
    """
    The civ_fit is a list with data in the following format: {
        'civ': X1
        'played': X3,
        'wins': X4
        'win_chance': X5,
        'points': X6
    }
    """
    stats_civ_fit = ndb.PickleProperty(default=None)
    setting_default_trebuchet_allowed = ndb.BooleanProperty(default=False)
    setting_default_rule = ndb.KeyProperty(kind='Rule', default=None)

    def rating(self):
        """ To avoid hitting the db unneccessary the rating value is stored in memory.
        """
        if hasattr(self, "_current_rating_cached"):
            return self._current_rating_cached
        else:
            self._current_rating_cached = PlayerResult.get_last_stats_rating(self.key)
            return self._current_rating_cached

    def set_new_rating_adjustment(self, new_rating_adjustment):
        rating_adjustment_dif = new_rating_adjustment - self.rating_adjustment
        all_other_players = Player.query(Player.key != self.key).fetch()
        rating_change_per_loop_value = 1 if rating_adjustment_dif < 0 else -1

        # Divide the adjustment +/-1 at a time for safety
        i = 0
        while rating_adjustment_dif != 0:
            all_other_players[i].rating_adjustment += rating_change_per_loop_value
            rating_adjustment_dif += rating_change_per_loop_value
            self.rating_adjustment -= rating_change_per_loop_value
            if i == len(all_other_players)-1:
                i = 0
            else:
                i += 1

        # Verify that the sum of all rating adjustments are 0
        all_players = all_other_players + [self]
        sum = 0
        for player in all_players:
            sum += player.rating_adjustment
        if sum != 0:
            raise Exception("Setting new rating adjustment algorithm failed. Total rating adjustment among all players is not 0.")

        # Validation passed -> save now
        for player in all_players:
            player.put()

    def get_data(self, data_detail="simple"):
        data = {}
        if data_detail in ["simple", "full"]:
            data.update(self._get_base_data())
        if data_detail == "full":
            data.update(self._get_stats_data())
        return data

    def _get_base_data(self):
        played = PlayerResult.query(PlayerResult.player == self.key).count()
        wins = PlayerResult.query(PlayerResult.player == self.key, PlayerResult.is_winner == True).count()
        
        return {
            'id': self.key.id(), 
            'nick': self.nick, 
            'rating': self.rating(),
            'rating_adjustment': self.rating_adjustment,
            'played': played,
            'wins': wins,
            'win_chance': None if played == 0 else int(wins * 100.0 / played),
            'claimed': True if self.userid else False,
            'verified': True if self.verified == True else False,
            'active': self.active,
            'rating_change_prev_round': self._get_rating_change_previous_round(), # Only used for league, might need to further limit when this loads
            'settings': {
                'default_trebuchet_allowed': self.setting_default_trebuchet_allowed,
                'default_rule': self.setting_default_rule.id() if self.setting_default_rule else None
            }
        }
        
    def _get_rating_change_previous_round(self):
        newest_player_result = PlayerResult.query(PlayerResult.player == self.key).order(-PlayerResult.game_date).get()
        if not newest_player_result:
            return "0"

        newest_game_session_result = PlayerResult.query().order(-PlayerResult.game_date).get()
        if not newest_game_session_result:
            return "0"
        else:
            newest_game_session_date = newest_game_session_result.game_date

        previous_round_date = newest_game_session_date - timedelta(days=5)
        previous_round = PlayerResult.query(PlayerResult.player == self.key, PlayerResult.game_date < previous_round_date).order(-PlayerResult.game_date).get()

        if previous_round:
            previous_rating = previous_round.stats_rating
        else:
            previous_rating = PLAYER_RATING_START_VALUE + self.rating_adjustment

        return newest_player_result.stats_rating - previous_rating
        
    def _get_stats_data(self):
        if not self.calc_and_update_stats_if_needed():
            return {}
        return {
            'stats': {
                'average_score': self.stats_average_score,
                'average_score_per_min': round(self.stats_average_score_per_min, 1),
                'best_score': {
                    'value': self.stats_best_score,
                    'game_id': self.stats_best_score_game.id()
                },
                'worst_score': {
                    'value': self.stats_worst_score,
                    'game_id': self.stats_worst_score_game.id()
                },
                'best_score_per_min': {
                    'value': round(self.stats_best_score_per_min, 1),
                    'game_id': self.stats_best_score_per_min_game.id()
                },
                'worst_score_per_min': {
                    'value': round(self.stats_worst_score_per_min, 1),
                    'game_id': self.stats_worst_score_per_min_game.id()
                },
                'percentage_topping_score': self.stats_percentage_topping_score,
                'longest_winning_streak': self.stats_longest_winning_streak,
                'longest_losing_streak': self.stats_longest_losing_streak,
                'teammate_fit': self.stats_teammate_fit,
                'enemy_fit': self.stats_enemy_fit,
                'civ_fit': self.stats_civ_fit
            }
        }

    def calc_and_update_stats_if_needed(self):
        if self.stats_average_score is None:
            player_results = PlayerResult.query(PlayerResult.player == self.key).order(PlayerResult.game_date).fetch()
            if len(player_results) == 0:
                return False
            self._calc_stats_score_related(player_results)
            self._calc_stats_best_civ(player_results)
            self._calc_stats_worst_civ(player_results)
            self._calc_stats_streaks(player_results)
            self._calc_stats_teammate_fit(player_results)
            self._calc_stats_enemy_fit(player_results)
            self._calc_stats_civ_fit(player_results)
            self.put()
            return True
        return True

    def _calc_stats_score_related(self, player_results):
        self.stats_best_score = 0
        self.stats_best_score_game = None
        self.stats_worst_score = 999999
        self.stats_worst_score_game = None
        
        self.stats_best_score_per_min = 0
        self.stats_best_score_per_min_game = None
        self.stats_worst_score_per_min = 999999
        self.stats_worst_score_per_min_game = None
        
        total_score = 0
        total_seconds = 0
        topped_score_while_in_team = 0
        for res in player_results:
            related_game = res.game.get()
            total_score += res.score
            total_seconds += related_game.duration_seconds
            score_per_min = res.score / (related_game.duration_seconds / 60.0)
            if res.score > self.stats_best_score:
                self.stats_best_score = res.score
                self.stats_best_score_game = res.game
            if res.score < self.stats_worst_score:
                self.stats_worst_score = res.score
                self.stats_worst_score_game = res.game
            if score_per_min > self.stats_best_score_per_min:
                self.stats_best_score_per_min = score_per_min
                self.stats_best_score_per_min_game = res.game
            if score_per_min < self.stats_worst_score_per_min:
                self.stats_worst_score_per_min = score_per_min
                self.stats_worst_score_per_min_game = res.game
            # Score topping?
            team_mates_results = PlayerResult.query(PlayerResult.game == res.game, PlayerResult.team == res.team).fetch()
            if len(team_mates_results) > 1:
                if res.score == max([team_mate_res.score for team_mate_res in team_mates_results]):
                    topped_score_while_in_team += 1
            
        self.stats_average_score = total_score / len(player_results)
        self.stats_average_score_per_min = total_score / (total_seconds / 60.0)
        self.stats_percentage_topping_score = topped_score_while_in_team * 100 / len(player_results)
        
    def _calc_stats_best_civ(self, player_results):
        civ_won_dict = {}
        for result in player_results:
            if result.is_winner:
                if not civ_won_dict.has_key(result.civilization):
                    civ_won_dict[result.civilization] = 0
                civ_won_dict[result.civilization] += 1
        
        if len(civ_won_dict) > 0:
            best_civ = max(civ_won_dict.iteritems(), key=operator.itemgetter(1))[0]
            self.stats_civ_most_wins_name = best_civ
            self.stats_civ_most_wins_count = civ_won_dict[best_civ]
    def _calc_stats_worst_civ(self, player_results):
        civ_lost_dict = {}
        for result in player_results:
            if result.is_winner == False:
                if not civ_lost_dict.has_key(result.civilization):
                    civ_lost_dict[result.civilization] = 0
                civ_lost_dict[result.civilization] += 1
        
        if len(civ_lost_dict) > 0:
            worst_civ = max(civ_lost_dict.iteritems(), key=operator.itemgetter(1))[0]
            self.stats_civ_most_losses_name = worst_civ
            self.stats_civ_most_losses_count = civ_lost_dict[worst_civ]

    def _calc_stats_streaks(self, player_results):
        self.stats_longest_winning_streak = 0
        self.stats_longest_losing_streak = 0
        current_winning_streak = 0
        current_losing_streak = 0
        for result in player_results:
            if result.is_winner:
                current_losing_streak = 0
                current_winning_streak += 1
                self.stats_longest_winning_streak = max(self.stats_longest_winning_streak, current_winning_streak)
            else:
                current_winning_streak = 0
                current_losing_streak += 1
                self.stats_longest_losing_streak = max(self.stats_longest_losing_streak, current_losing_streak)

    def _calc_stats_teammate_fit(self, player_results):
        # First map wins and played to teammate_fit
        teammate_fit = {}
        for res in player_results:
            if res.team:
                game_duration_seconds = res.game.get().duration_seconds
                team_mates_results = PlayerResult.query(PlayerResult.game == res.game, PlayerResult.team == res.team, PlayerResult.player != res.player).fetch()
                for team_mate_res in team_mates_results:
                    teammate_id = team_mate_res.player.id()
                    if not teammate_fit.has_key(teammate_id):
                        teammate_fit[teammate_id] = {'teammate': {'id': teammate_id}, 'played': 0, 'wins': 0, 'total_duration_seconds': 0, 'total_score': 0}
                    teammate_fit[teammate_id]['played'] += 1
                    teammate_fit[teammate_id]['total_duration_seconds'] += game_duration_seconds
                    teammate_fit[teammate_id]['total_score'] += res.score
                    if res.is_winner:
                        teammate_fit[teammate_id]['wins'] += 1
        # Convert to list, add player nick to info and calc win chance
        teammate_fit_list = []
        for teammate_id, teammate_dict in teammate_fit.iteritems():
            teammate_dict['win_chance'] = int(teammate_dict['wins'] * 100.0 / teammate_dict['played'])
            teammate_dict['score_per_min'] = round(teammate_dict['total_score'] / (teammate_dict['total_duration_seconds'] / 60.0), 1)
            teammate_dict['teammate']['nick'] = Player.get_by_id(teammate_dict['teammate']['id']).nick
            teammate_dict['points'] = _fit_points(teammate_dict['wins'], teammate_dict['played'])
            teammate_fit_list.append(teammate_dict)
        self.stats_teammate_fit = teammate_fit_list
        
    def _calc_stats_enemy_fit(self, player_results):
        # First map wins and played to enemy_fit
        enemy_fit = {}
        for res in player_results:
            game_duration_seconds = res.game.get().duration_seconds
            other_results = PlayerResult.query(PlayerResult.game == res.game, PlayerResult.player != res.player).fetch()
            for other_res in other_results:
                if other_res.team is not None and other_res.team == res.team:
                    continue
                enemy_id = other_res.player.id()
                if not enemy_fit.has_key(enemy_id):
                    enemy_fit[enemy_id] = {'enemy': {'id': enemy_id}, 'played': 0, 'wins': 0, 'total_duration_seconds': 0, 'total_score': 0}
                enemy_fit[enemy_id]['played'] += 1
                enemy_fit[enemy_id]['total_duration_seconds'] += game_duration_seconds
                enemy_fit[enemy_id]['total_score'] += res.score
                if res.is_winner:
                    enemy_fit[enemy_id]['wins'] += 1
        # Convert to list, add player nick to info and calc win chance
        enemy_fit_list = []
        for enemy_id, enemy_dict in enemy_fit.iteritems():
            enemy_dict['win_chance'] = int(enemy_dict['wins'] * 100.0 / enemy_dict['played'])
            enemy_dict['score_per_min'] = round(enemy_dict['total_score'] / (enemy_dict['total_duration_seconds'] / 60.0), 1)
            enemy_dict['enemy']['nick'] = Player.get_by_id(enemy_dict['enemy']['id']).nick
            enemy_dict['points'] = _fit_points(enemy_dict['wins'], enemy_dict['played'])
            enemy_fit_list.append(enemy_dict)
        self.stats_enemy_fit = enemy_fit_list

    def _calc_stats_civ_fit(self, player_results):
        # First map wins and played to the civs
        civ_fit = {}
        for res in player_results:
            game_duration_seconds = res.game.get().duration_seconds
            if not civ_fit.has_key(res.civilization):
                civ_fit[res.civilization] = {'civ': res.civilization, 'played': 0, 'wins': 0, 'total_duration_seconds': 0, 'total_score': 0}
            civ_fit[res.civilization]['played'] += 1
            civ_fit[res.civilization]['total_duration_seconds'] += game_duration_seconds
            civ_fit[res.civilization]['total_score'] += res.score
            if res.is_winner:
                civ_fit[res.civilization]['wins'] += 1
        # Convert to list and calc win_chance
        civ_fit_list = []
        for civ_name, civ_dict in civ_fit.iteritems(): 
            civ_dict['win_chance'] = int(civ_dict['wins'] * 100.0 / civ_dict['played'])
            civ_dict['score_per_min'] = round(civ_dict['total_score'] / (civ_dict['total_duration_seconds'] / 60.0), 1)
            civ_dict['points'] = _fit_points(civ_dict['wins'], civ_dict['played'])
            civ_fit_list.append(civ_dict)
        self.stats_civ_fit = civ_fit_list

    def clear_stats(self):
        for variable_name in self.__dict__['_values'].keys():  # __dict__['_values'] contains all class object variables
            if 'stats_' in variable_name:
                setattr(self, variable_name, None)
        self.put()




class Rule(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    creator = ndb.KeyProperty(kind=Player, required=True)

    def get_data(self):
        return {
            'id': self.key.id(),
            'name': self.name,
            'description': self.description,
            'creator': {'id': self.creator.id(), 'nick': self.creator.get().nick}
        }


class Game(ndb.Model):
    rule = ndb.KeyProperty(kind=Rule, default=None)
    # After finish values
    date = ndb.DateTimeProperty(required=False)
    duration_seconds = ndb.IntegerProperty(required=False)
    # Settings from lobby Game Settings
    game_type = ndb.StringProperty(required=False, choices=['Random Map', 'Turbo Random Map', 'Regicide', 'Death Match', 'Scenario', 'King of the Hill', 'Wonder Race', 'Defend the Wonder', 'Capture the Relic', 'Sudden Death'])
    size = ndb.StringProperty(required=False, choices=['Tiny (2 player)', 'Small (3 player)', 'Medium (4 player)', 'Normal (6 player)', 'Large (8 player)', 'Giant', 'LudiKRIS'])
    difficulty = ndb.StringProperty(required=False, choices=['Easiest', 'Standard', 'Moderate', 'Hard', 'Hardest'])
    resources = ndb.StringProperty(required=False, choices=['Standard', 'Low', 'Medium', 'High'])
    population = ndb.IntegerProperty(required=False, choices=[25, 50, 75, 100, 125, 150, 175, 200, 300, 400, 500])
    game_speed = ndb.StringProperty(required=False, choices=['Slow', 'Normal', 'Fast'])
    reveal_map = ndb.StringProperty(required=False, choices=['Normal', 'Explored', 'All Visible'])
    starting_age = ndb.StringProperty(required=False, choices=['Standard','Dark Age', 'Feudual Age', 'Castle Age', 'Imperial Age', 'Post-Imperial Age'])
    treaty_length = ndb.IntegerProperty(required=False, choices=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 90])
    victory = ndb.StringProperty(required=False, choices=['Standard', 'Conquest', 'Time Limit', 'Score', 'Last Man Standing'])
    team_together = ndb.BooleanProperty(required=False)
    all_techs = ndb.BooleanProperty(required=False)
    # Settings from Objective screen ingame
    location = ndb.StringProperty(required=False, choices=['Arabia', 'Archipelago', 'Arena', 'Baltic', 'Black Forest', 'Coastal', 'Continental', 'Crater Laker', 'Fortress', 'Ghost Lake', 'Gold Rush', 'Highland', 'Islands', 'Mediterranean', 'Migration', 'Mongolia', 'Nomad', 'Oasis', 'Rivers', 'Salt Marsh', 'Scandinavia', 'Team Islands', 'Yucatan', 'Acropolis', 'Budapest', 'Cenotes', 'City of Lakes', 'Golden Pit', 'Hideout', 'Hill Fort', 'Lombardia', 'Steppe', 'Valley', 'MegaRandom', 'Hamburger', 'Canyons', 'Enemy Archipelago', 'Enemy Islands', 'Far Out', 'Front Line', 'Inner Circle', 'Motherland', 'Open Plains', 'Ring of Water', 'Snakepit', 'The Eye'])
    # Special settings
    trebuchet_allowed = ndb.BooleanProperty(required=False)
    # Values that are not neccesarry to store but stored to avoid having to recompute values every time the value is needed
    derived_game_format = ndb.StringProperty(required=False)

    def game_format(self):
        if self.derived_game_format:
            return self.derived_game_format
        else:
            player_results = [res.get_data() for res in PlayerResult.query(PlayerResult.game==self.key)]
            teams = [player_data['team'] for player_data in player_results]
            counted_teams = Counter(teams)
            game_format = ""
            # First add people with teams, sorted by the most common
            for key, value in counted_teams.most_common():
                if key is None: # People without teams is dealth with afterwards so v1v1.. is at the end
                    pass
                else:
                    game_format += "%sv" % value
            # Then add the teamless as v1v1v1v1.. etc
            for _ in range(counted_teams[None]):
                game_format += "1v"
            # Return all but extra v
            self.derived_game_format = game_format[:-1]
            self.put()
            return self.derived_game_format

    def get_data(self, data_detail="simple"):  
        data = {}
        if data_detail in ["simple", "full"]:
            data.update({
                'id': self.key.id(),
                'title': "%s %s" % (self.game_type, self.location),
                'team_format': self.game_format(),
                'date_epoch': _date_to_epoch(self.date),
                'game_type': self.game_type,
            })
            
        if data_detail == "full":
            data.update({
                'duration_seconds': self.duration_seconds,
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
                'player_results': [res.get_data() for res in PlayerResult.query(PlayerResult.game==self.key)],
                'rule': self.rule.get().get_data() if self.rule else None
            })
        return data

    @classmethod
    def settings_data(cls):
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
    score = ndb.IntegerProperty(required=True)
    team = ndb.IntegerProperty(choices=[1,2,3,4])
    civilization = ndb.StringProperty(required=True, choices=CIVILIZATIONS)
    stats_rating = ndb.IntegerProperty(required=True)

    @classmethod
    def settings_data(cls):
        return {
            'teams': list(cls.team._choices),
            'civilizations': list(cls.civilization._choices)
        }

    @classmethod
    def get_last_stats_rating(cls, player_key):
        last_result = PlayerResult.query(PlayerResult.player == player_key).order(-PlayerResult.game_date).get()
        if last_result:
            return last_result.stats_rating
        else: # Is first player result calculating for
            return PLAYER_RATING_START_VALUE + player_key.get().rating_adjustment

    def get_previous_stats_rating(self):
        previous_result = PlayerResult.query(PlayerResult.player == self.player, PlayerResult.game_date < self.game_date).order(-PlayerResult.game_date).get()
        if previous_result:
            return previous_result.stats_rating
        else:
            return PLAYER_RATING_START_VALUE + self.player.get().rating_adjustment

    def get_data(self):
        player = self.player.get()
        return{
            'player': {'id': player.key.id(), 'nick': player.nick},
            'game': self.game.id(),
            'is_winner': self.is_winner,
            'score': self.score,
            'team': self.team,
            'civilization': self.civilization,
            'stats_rating': self.stats_rating,
            'rating_earned': self.rating_earned()
        }

    def rating_earned(self):
        return self.stats_rating - self.get_previous_stats_rating()


class CivilizationStats(ndb.Model):
    name = ndb.StringProperty(required=True, choices=CIVILIZATIONS)
    played = ndb.IntegerProperty()
    wins = ndb.IntegerProperty()
    win_chance = ndb.IntegerProperty()
    average_score_per_min = ndb.FloatProperty()
    player_fit = ndb.PickleProperty()

    def get_data(self):
        data = {
            'name': self.name
        }
        data.update(self._get_stats_data())
        return data

    def _get_stats_data(self):
        if not self.calc_and_update_stats_if_needed():
            return {}
        else:
            return {
                'stats': {
                    'played': self.played,
                    'wins': self.wins,
                    'points': _fit_points(self.wins, self.played),
                    'win_chance': self.win_chance,
                    'average_score_per_min': round(self.average_score_per_min, 1),
                    'player_fit': self.player_fit
                }
        }

    def calc_and_update_stats_if_needed(self):
        if self.played is None:
            player_results = PlayerResult.query(PlayerResult.civilization == self.name).fetch()
            if len(player_results) == 0:
                return False
            self._calc_stats_basic(player_results)
            self._calc_stats_player_fit(player_results)
            self.put()
            return True
        return True

    def _calc_stats_basic(self, player_results):
        self.played = 0
        self.wins = 0

        total_score = 0
        total_seconds = 0
        for res in player_results:
            related_game = res.game.get()
            total_score += res.score
            total_seconds += related_game.duration_seconds
            self.played += 1
            if res.is_winner:
                self.wins += 1

        self.win_chance = int(self.wins * 100.0 / self.played)
        self.stats_average_score = total_score / len(player_results)
        self.average_score_per_min = total_score / (total_seconds / 60.0)

    def _calc_stats_player_fit(self, player_results):
        # First map wins and played to the players
        player_fit = {}
        for res in player_results:
            player_id = res.player.id()
            if not player_fit.has_key(player_id):
                player_fit[player_id] = {'player': {'id': player_id}, 'played': 0, 'wins': 0}
            player_fit[player_id]['played'] += 1
            if res.is_winner:
                player_fit[player_id]['wins'] += 1
        # Convert to list and calc win_chance
        player_fit_list = []
        for player_id, player_dict in player_fit.iteritems():
            player_dict['win_chance'] = int(player_dict['wins'] * 100.0 / player_dict['played'])
            player_dict['points'] = _fit_points(player_dict['wins'], player_dict['played'])
            player_dict['player']['nick'] = Player.get_by_id(player_dict['player']['id']).nick
            player_fit_list.append(player_dict)
        self.player_fit = player_fit_list


def _fit_points(wins, played):
    return (wins * 2) - played


def _date_to_epoch(date_value):
    """ Duplicate of utils method, but added here because of potential circular reference between models.py and utils.py
    """
    return int((date_value - datetime(1970,1,1)).total_seconds())

# class GlobalStats(ndb.Model):
#     worst_couple_player1 = ndb.KeyProperty(kind=Player)
#     worst_couple_player2 = ndb.KeyProperty(kind=Player)
#     best_couple_player1 = ndb.KeyProperty(kind=Player)
#     best_couple_player2 = ndb.KeyProperty(kind=Player)
#     most_frequent_score_topper_player = ndb.KeyProperty(kind=Player)
#     most_frequent_score_topper_games = ndb.IntegerProperty()
#     most_frequent_score_topper_of_total = ndb.IntegerProperty()