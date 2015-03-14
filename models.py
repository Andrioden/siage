from google.appengine.ext import ndb
import datetime
from collections import Counter
from config import PLAYER_RATING_START_VALUE

class Player(ndb.Model):
    nick = ndb.StringProperty(required=True)
    
    def get_data(self):
        last_player_result = PlayerResult._last_result(self.key)
        return {
            'id': self.key.id(), 
            'nick': self.nick, 
            'rating': (0 if last_player_result == None else last_player_result.stats_rating),
            'played': PlayerResult.query(PlayerResult.player==self.key).count(),
            'wins': PlayerResult.query(PlayerResult.player==self.key, PlayerResult.is_winner==True).count(),
        }

class Game(ndb.Model):
    # After finish values
    date = ndb.DateTimeProperty(required=False)
    duration_seconds = ndb.IntegerProperty(required=False)
    # Settings from lobby Game Settings
    game_type = ndb.StringProperty(required=False, choices=['Random Map', 'Turbo Random Map', 'Regicide', 'Death Match', 'Scenario', 'King of the Hill', 'Wonder Race', 'Defend the Wonder', 'Capture the Relic'])
    size = ndb.StringProperty(required=False, choices=['Tiny (2 player)', 'Small (3 player)', 'Medium (3 player)', 'Normal (6 player)', 'Large (8 player)', 'Giant', 'LudiKRIS'])
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
        game_format = None
        # First add people with teams, sorted by the most common
        for key, value in counted_teams.most_common():
            if key == None: # People without teams is dealth with afterwards so v1v1.. is at the end
                pass
            elif game_format == None: # First
                game_format = "%s" % value
            else:
                game_format += "v%s" % value
        # Then add the teamless as v1v1v1v1.. etc
        for _ in range(counted_teams[None]):
            game_format += "v1"
        return game_format
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
    is_winner = ndb.BooleanProperty(default=False)
    score = ndb.IntegerProperty(required=True)
    team = ndb.IntegerProperty(choices=[1,2,3,4])
    civilization = ndb.StringProperty(required=True, choices=['Aztec', 'Britons', 'Byzantines', 'Celts', 'Chinese', 'Franks', 'Goths', 'Huns', 'Incas', 'Indians', 'Italians', 'Japanese', 'Koreans', 'Magyars', 'Mayans', 'Mongols', 'Persians', 'Saracens', 'Slavs', 'Spanish', 'Teutons', 'Turks', 'Vikings'])
    stats_rating = ndb.IntegerProperty(required=True)
    next_player_result = ndb.KeyProperty(kind='PlayerResult', default=None) # 'PlayerResult' is a string to allow circular reference.
    @classmethod
    def _settings_data(cls):
        return {
            'teams': list(cls.team._choices),
            'civilizations': list(cls.civilization._choices)
        }
    @classmethod
    def _last_result(cls, player_key):
        """ This can be considered a static method, which is called a class method. It is just a
        helper method to get the last PlayerResult instance for a given player key. It does not work
        on the instance.
        """
        last_player_result_query = cls.query(cls.player == player_key, cls.next_player_result == None)
        if last_player_result_query.count() > 1:
            raise Exception("Attempted to get last player result for player %s, found %s PlayerResult without next_stats set. Should only be 1." % (player_key.get().nick, last_player_result_query.count()))
        else:
            return last_player_result_query.get()
    def get_data(self):
        player_entity = self.player.get()
        return{
            'player': {'id': player_entity.key.id(), 'nick': player_entity.nick},
            'game': self.game.id(),
            'is_winner': self.is_winner,
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
    def get_previous_result(self):
        return PlayerResult.query(PlayerResult.next_player_result==self.key).get()