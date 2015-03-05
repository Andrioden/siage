import webapp2
import json
from models import Game
from models import PlayerResult

class GameSettingsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        all_settings = Game._settings_data()
        all_settings.update(PlayerResult._settings_data())
        self.response.out.write(json.dumps(all_settings))

app = webapp2.WSGIApplication([
    (r'/api/gamesettings/', GameSettingsHandler)
], debug=True)