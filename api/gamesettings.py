import webapp2
import json
from models import *
from utils import *


class GameSettingsHandler(webapp2.RequestHandler):
    def get(self):
        all_settings = Game.settings_data()
        all_settings.update(PlayerResult.settings_data())
        all_settings['players'] = self._get_players_id_and_nick()
        all_settings['rules'] = self._get_rules_id_and_name()
        set_json_response(self.response, all_settings)

    def _get_players_id_and_nick(self):
        return [player.get_data_id_and_nick() for player in Player.query().fetch(projection=[Player.nick])]

    def _get_rules_id_and_name(self):
        return [rule.get_data_id_and_name() for rule in Rule.query().fetch(projection=[Rule.name])]


app = webapp2.WSGIApplication([
    (r'/api/gamesettings/', GameSettingsHandler)
], debug=True)
