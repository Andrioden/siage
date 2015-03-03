import webapp2
import json
import models

class GameSettingsHandler(webapp2.RequestHandler):
    def get(self, settingname=None):
        self.response.headers['Content-Type'] = 'application/json'

        if settingname == 'gametypes':
            obj = [
                {'id': '1', 'label': 'Game type 1'},
                {'id': '2', 'label': 'Game type 2'},
                {'id': '3', 'label': 'Game type 3'}
            ]
        elif settingname == 'mapstyles':
            obj = [
                {'id': '1', 'label': 'Map style 1'},
                {'id': '2', 'label': 'Map style 2'},
                {'id': '3', 'label': 'Map style 3'}
            ]

        elif settingname == 'civilizations':
            obj = [
                {'id': '1', 'label': 'Aztecs'},
                {'id': '2', 'label': 'Britons'},
                {'id': '3', 'label': 'Byzantines'},
                {'id': '4', 'label': 'Celts'},
                {'id': '5', 'label': 'Chinese'},
                {'id': '6', 'label': 'Franks'},
                {'id': '7', 'label': 'Goths'},
                {'id': '8', 'label': 'Huns'},
                {'id': '9', 'label': 'Incas'},
                {'id': '10', 'label': 'Indians'},
                {'id': '11', 'label': 'Italians'},
                {'id': '12', 'label': 'Japanese'},
                {'id': '13', 'label': 'Koreans'},
                {'id': '14', 'label': 'Magyars'},
                {'id': '15', 'label': 'Mayans'},
                {'id': '16', 'label': 'Mongols'},
                {'id': '17', 'label': 'Persians'},
                {'id': '18', 'label': 'Saracens'},
                {'id': '19', 'label': 'Slavs'},
                {'id': '10', 'label': 'Spanish'},
                {'id': '21', 'label': 'Teutons'},
                {'id': '22', 'label': 'Turks'},
                {'id': '23', 'label': 'Vikings'}
            ]
        else:
            obj = [
                {'id': '1', 'label': 'Test1'},
                {'id': '2', 'label': 'Test2'},
                {'id': '3', 'label': 'Test3'}
            ]


        self.response.out.write(json.dumps(obj))


app = webapp2.WSGIApplication([
    webapp2.Route(r'/api/gamesettings/<settingname>', handler=GameSettingsHandler, name='gamesetting')
], debug=True)