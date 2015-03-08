from google.appengine.ext import ndb

class Player(ndb.Model):
    nick = ndb.StringProperty(required=True)
    
    def get_data(self):
        player_result = PlayerResult._last_result(self.key)
        if player_result:
            rating = player_result.stats_rating
        else:
            rating = 0
        
        return {
            'id': self.key.id(), 
            'nick': self.nick, 
            'rating': '?????' #TODO
        }

class Game(ndb.Model):
    # Finish settings
    date = ndb.StringProperty(required=False)
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
    treaty_length = ndb.StringProperty(required=False, choices=['None', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '90'])
    victory = ndb.StringProperty(required=False, choices=['Standad', 'Conquest', 'Time Limit', 'Score', 'Last Man Standing'])
    team_together = ndb.StringProperty(required=False)
    all_techs = ndb.StringProperty(required=False)
    # Settings from Objective screen ingame
    map_type = ndb.StringProperty(required=False, choices=['typex', 'typey'])
    # Special settings
    trebuchet_allowed = ndb.StringProperty(required=False)
    def get_data(self):
        return {
            'id': self.key.id(),
            'date': self.date,
            'duration_seconds': self.duration_seconds,
            'title': self.game_type + ' ' + self.map_type,
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
            'map_type': self.map_type,
            'trebuchet_allowed': self.trebuchet_allowed
        }
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
            'treaty_length': list(cls.treaty_length._choices),
            'victory': list(cls.victory._choices),
            'map_types': list(cls.map_type._choices)
        }

class PlayerResult(ndb.Model):
    player = ndb.KeyProperty(kind=Player, required=True)
    game = ndb.KeyProperty(kind=Game, required=True)
    is_winner = ndb.BooleanProperty(default=False)
    score = ndb.IntegerProperty(required=True)
    team = ndb.IntegerProperty(required=True, choices=[0,1,2,3,4,5,6,7,8])
    civilization = ndb.StringProperty(required=True, choices=['Aztec', 'Franks'])
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
        last_player_result_query = cls.query(cls.player == player_key, cls.next_player_result == None)
        if last_player_result_query.count() > 1:
            raise Exception("Attempted to get last player result for player %s, found %s PlayerResult without next_stats set. Should only be 1." % (player_key.get().nick, last_player_result_query.count()))
        else:
            return last_player_result_query.get()

    @classmethod
    def get_data(self):
        return{
            'player': self.player,
            'game': self.game,
            'is_winner': self.is_winner,
            'score': self.score,
            'team': self.team,
            'civilization': self.civilization,
            'stats_rating': self.stats_rating,
            'next_player_result': self.next_player_result
        }