import webapp2
import json
from models import Game
from models import PlayerResult

class GameSettingsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        allSettings = Game._settings_data()
        allSettings.update(PlayerResult._playerresult_settings_data())
        self.response.out.write(json.dumps(allSettings))

app = webapp2.WSGIApplication([
    (r'/api/gamesettings/', GameSettingsHandler)
], debug=True)