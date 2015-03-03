from google.appengine.ext import ndb

class Player(ndb.Model):
    nick = ndb.StringProperty(required=True)
    
    def get_data(self):
        return {'id': self.key.id(), 'nick': self.nick}

class Game(ndb.Model):
    date = ndb.DateProperty(required=True)
    game_type = ndb.StringProperty(required=True, choices=['GameType 1', 'GameType 2'])
    map_size = ndb.StringProperty(required=True, choices=['small', 'LOL', 'big'])
    map_type = ndb.StringProperty(required=True, choices=['typex', 'typey'])
    starting_age = ndb.StringProperty(required=True, choices=['Dark Age', 'Feudual Age', 'Castle Age', 'Imperial Age'])
    resources = ndb.StringProperty(required=True, choices=['low'])
    difficulty = ndb.StringProperty(required=True, choices=['easy'])
    fixed_position = ndb.BooleanProperty(required=True)
    reveal_map = ndb.BooleanProperty(required=True)
    full_technology = ndb.BooleanProperty(required=True)
    population = ndb.IntegerProperty(required=True, choices=[50,100,200])
    duration_seconds = ndb.IntegerProperty(required=True)
    trebuchet_allowed = ndb.BooleanProperty(required=True)
    @classmethod
    def _settings_data(cls):
        return {
            'game_types': list(cls.game_type._choices),
            'map_size': list(cls.map_type._choices),
            'map_type': list(cls.map_type._choices),
            'starting_age': list(cls.starting_age._choices),
            'resources': list(cls.resources._choices),
            'difficulty': list(cls.difficulty._choices),
            'population': list(cls.population._choices)
        }
    
class PlayerResult(ndb.Model):
    player = ndb.KeyProperty(required=True, kind=Player)
    game = ndb.KeyProperty(required=True, kind=Game)
    is_winner = ndb.BooleanProperty(default=False)
    score = ndb.IntegerProperty(required=True)
    civilization = ndb.StringProperty(required=True, choices=['Aztec', 'Franks'])
    
class PlayerResultStats(ndb.Model):
    player_result = ndb.KeyProperty(required=True, kind=PlayerResult)
    rating = ndb.IntegerProperty(required=True)