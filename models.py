from google.appengine.ext import ndb

class Player(ndb.Model):
    nick = ndb.StringProperty(required=True)
    
    def get_data(self):
        return {'id': self.key.id(), 'nick': self.nick}

class Game(ndb.Model):
    # Finish settings
    date = ndb.DateProperty(required=False)
    duration_seconds = ndb.IntegerProperty(required=False)
    # Settings from lobby Game Settings
    game_type = ndb.StringProperty(required=False, choices=['Random Map', 'Death Match'])
    size = ndb.StringProperty(required=False, choices=['small', 'LOL', 'big'])
    difficulty = ndb.StringProperty(required=False, choices=['Standard', '??'])
    resources = ndb.StringProperty(required=False, choices=['Standard', '??'])
    population = ndb.IntegerProperty(required=False, choices=[50,100,200])
    game_speed = ndb.StringProperty(required=False, choices=['Slow', 'Normal', 'Fast'])
    reveal_map = ndb.BooleanProperty(required=False)
    starting_age = ndb.StringProperty(required=False, choices=['Dark Age', 'Feudual Age', 'Castle Age', 'Imperial Age'])
    treaty_length = ndb.StringProperty(required=False, choices=['None', '????'])
    victory = ndb.StringProperty(required=False, choices=['Conquest'])
    team_together = ndb.BooleanProperty(required=False)
    all_techs = ndb.BooleanProperty(required=False)
    # Settings from Objective screen ingame
    map_type = ndb.StringProperty(required=False, choices=['typex', 'typey'])
    # Special settings
    trebuchet_allowed = ndb.BooleanProperty(required=False)
    def get_data(self):
        return {
            'id': self.key.id(),
            'title': "fuck dea %s" % self.key.id(),
            'game_type': self.game_type
        }
    @classmethod
    def _settings_data(cls):
        return {
            #TODO add alle, rename til size(S)SSS
            'game_types': list(cls.game_type._choices),
            'map_size': list(cls.size._choices), #rename til size
            'map_type': list(cls.map_type._choices),
            'starting_age': list(cls.starting_age._choices),
            'resources': list(cls.resources._choices),
            'difficulty': list(cls.difficulty._choices),
            'population': list(cls.population._choices),
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