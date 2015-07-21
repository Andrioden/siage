import math
from operator import attrgetter
import logging
from config import *

class RatingCalculator:
    def __init__(self):
        self.player_results = []

    def add_player_results_from_dict(self, player_results_dict):
        from models import PlayerResult, Player # On demand loading modules because they break the tests
        from google.appengine.ext import ndb # On demand loading modules because they break the tests

        for player_res_dict in player_results_dict:
            player_key = ndb.Key(Player, int(player_res_dict['player_id']))
            last_rating = PlayerResult.get_last_stats_rating(player_key)
            self.player_results.append(RatingPlayerResult(player_key.id(), player_res_dict['is_winner'], player_res_dict['score'], player_res_dict['team'], last_rating))
    
    def calc_and_get_new_rating_dict(self):
        self._calc_ratings()
        new_ratings = {}
        for res in self.player_results:
            new_ratings[res.player_id] = res.new_rating
        return new_ratings
    
    def _calc_ratings(self):
        """
        1. Find total rating among all players
        2. Find teams total rating. Also adds single team players
        3. Find chance to win for team
        4. Find gain/lost using K-factor
        5. Adjust rating change according to amount of teams
        6. If playing in a team adjust according to score
        7. Give/take point if a rounding error was produced to top/bottom scorer.
        
        """
        self._validate_winner_list()
        
        # 1. Find total rating among all players
        # 2. Find teams total rating. Also adds single team players
        total_rating = 0
        team_ratings = {}
        for res in self.player_results:
            total_rating += res.prev_rating
            if res.team:
                team_key = 't_%s' % res.team
                if team_ratings.has_key(team_key):
                    team_ratings[team_key] = team_ratings[team_key] + res.prev_rating
                else:
                    team_ratings[team_key] = res.prev_rating
            else:
                team_ratings['p_%s' % res.player_id] = res.prev_rating
        
#         print "Total rating: %s" % total_rating
#         print "Team ratings: %s" % team_ratings
        
        for res in self.player_results:
            # 3. Find chance to win for team
            if res.team:
                team_rating = self._get_team_rating(res.team)
            else:
                team_rating = res.prev_rating
            
            win_chance = team_rating * 1.0 / total_rating
            
            # 4. Find gain/lost using K-factor
            if res.is_winner:
                team_rating_change = (1.0 - win_chance) * K_FACTOR
            else:
                team_rating_change = win_chance * -1.0 * K_FACTOR

            # 5. Adjust rating change according to amount of teams
            if self._get_amount_of_teams() > 2:
                team_rating_change = team_rating_change / 2

            # 6. If playing in a team adjust according to score
            player_team_size = self._get_team_size(res.team)
            if res.team and player_team_size > 1:
                base_rating_part = team_rating_change * (1.0 - SCORE_ADJUST_FACTOR) / player_team_size
                score_percent = res.score * 1.0 / self._get_team_score(res.team)
                if res.is_winner:
                    score_rating_part = team_rating_change * SCORE_ADJUST_FACTOR * score_percent
                else:
                    # I am not sure why this works mathematically, but it works on distributing a negative score in a favorish manner to the high scorers.
                    score_rating_part = team_rating_change * SCORE_ADJUST_FACTOR * (1.0 - score_percent) / (player_team_size - 1)
                player_rating_change =  int(round(base_rating_part + score_rating_part))
                # print "team_rating_change %s" % team_rating_change
                # print "base_rating_part %s" % base_rating_part
                # print "score_percent %s" % score_percent
                # print "score_rating_part %s" % score_rating_part
                # print "player_rating_change %s" % player_rating_change
            else:
                player_rating_change = int(round(team_rating_change))


            res.rating_change = player_rating_change
            res.new_rating = res.prev_rating + player_rating_change
            #logging.info("Team: %s | Player: %s | winchance: %s | team rating change: %s | player score %s | score adjusted rating: %s | rating: %s to %s " % (res.team, res.player_id, win_chance, team_rating_change, res.score, player_rating_change, res.prev_rating, res.new_rating))
            #print "Team: %s | Player: %s | winchance: %s | team rating change: %s | player score %s | score adjusted rating: %s | rating: %s to %s " % (res.team, res.player_id, win_chance, team_rating_change, res.score, player_rating_change, res.prev_rating, res.new_rating)
        # 7. Validate that an equal amount of rating have been lost as gained.
        #    If a difference is found. Give point from top score or remove from bottom.
        total_rating_change = sum(res.rating_change for res in self.player_results)
#         print "Total rating change before adjustments: %s" % total_rating_change
        if math.fabs(total_rating_change) > 2:
            raise Exception("Rating algorithm failed. To high difference between rating gained and lost.")
        
        if total_rating_change > 0:
            self._remove_rating_from_bottom_scored_player(int(math.fabs(total_rating_change)))
        elif total_rating_change < 0:
            self._add_rating_to_top_scored_player(int(math.fabs(total_rating_change)))
        
        total_rating_change = sum(res.rating_change for res in self.player_results)
        if total_rating_change != 0:
            #logging.info([str(res) for res in self.player_results])
            raise Exception("Rating algorithm failed. Difference between rating gained and lost after correction: %s" % total_rating_change)
            
    def _add_rating_to_top_scored_player(self, value):
        top_scored_player = max(self.player_results, key=attrgetter('score'))
        top_scored_player.new_rating += value
        top_scored_player.rating_change += value
        
    def _remove_rating_from_bottom_scored_player(self, value):
        bottom_scored_player = min(self.player_results, key=attrgetter('score'))
        bottom_scored_player.new_rating -= value
        bottom_scored_player.rating_change -= value
        
    def _get_team_rating(self, team):
        total_rating = 0
        for res in self.player_results:
            if res.team == team:
                total_rating += res.prev_rating
        return total_rating
    
    def _get_team_score(self, team):
        total_score = 0
        for res in self.player_results:
            if res.team == team:
                total_score += res.score
        return total_score
    
    def _get_team_size(self, team):
        size = 0
        for res in self.player_results:
            if res.team == team:
                size += 1
        return size

    def _get_amount_of_teams(self):
        amount = 0
        teams_counted = []
        for res in self.player_results:
            if res.team is None:
                amount += 1
            elif res.team and res.team not in teams_counted:
                amount += 1
                teams_counted.append(res.team)
        return amount

    def _validate_winner_list(self):
        winner_teams_or_players = []
        for res in self.player_results:
            if res.is_winner:
                if res.team:
                    winner_teams_or_players.append(res.team)
                else:
                    winner_teams_or_players.append(res.player_id)
        if len(set(winner_teams_or_players)) == 0:
            raise Exception("Validation Error: No winner.")
        elif len(set(winner_teams_or_players)) > 1:
            raise Exception("Validation Error: There is winners on multiple teams.")
    
class RatingPlayerResult:
    def __init__(self, player_id, is_winner, score, team, prev_rating):
        self.player_id = player_id
        self.is_winner = is_winner
        self.score = score
        self.prev_rating = prev_rating
        self.team = team
        self.new_rating = None
        self.rating_change = None
        
    def __str__(self):
        return "Player ID %s | Score: %s | new rating; %s | rating change: %s" % (self.player_id, self.score, self.new_rating, self.rating_change)
    
def recalculate_ratings():
    from models import PlayerResult, Game # On demand loading modules because they break the tests
    logging.info("----- RECALCULATING RATINGS ------")
    for game in Game.query().order(Game.date).fetch():
        logging.info("Recalculating for game %s" % game.key.id())
        game_player_results = PlayerResult.query(PlayerResult.game == game.key).fetch()
        # Recalc rating
        rc = RatingCalculator()
        for res in game_player_results:
            previous_rating = res.get_previous_stats_rating()
            rc.player_results.append(RatingPlayerResult(res.player.id(), res.is_winner, res.score, res.team, previous_rating))
        recalced_rating = rc.calc_and_get_new_rating_dict()
        # Update player result rating
        for res in game_player_results:
            res.stats_rating = recalced_rating[res.player.id()]
            res.put()