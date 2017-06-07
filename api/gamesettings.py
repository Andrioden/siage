import webapp2
import json
from models import Game
from models import PlayerResult
from utils import *


class GameSettingsHandler(webapp2.RequestHandler):
    def get(self):
        all_settings = Game.settings_data()
        all_settings.update(PlayerResult.settings_data())
        set_json_response(self.response, all_settings)


app = webapp2.WSGIApplication([
    (r'/api/gamesettings/', GameSettingsHandler)
], debug=True)
