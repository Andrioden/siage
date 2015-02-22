#!/usr/bin/env python

import webapp2
import json

class PlayersHandler(webapp2.RequestHandler):
    def get(self, playerId=None):
        self.response.headers['Content-Type'] = 'application/json'   
        obj = [
            {'nickname': 'Andrioden', 'rating': 1670, 'winrate': '55', 'bestcivilization': 'Huns'},
            {'nickname': 'Shrubber', 'rating': 1614, 'winrate': '51', 'bestcivilization': 'Mongols'}
        ]
        self.response.out.write(json.dumps(obj))

class GameTypesHandler(webapp2.RequestHandler):
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
                    {'id': '1', 'label': 'Byzantines'},
                    {'id': '1', 'label': 'Celts'},
                    {'id': '1', 'label': 'Chinese'},
                    {'id': '1', 'label': 'Franks'},
                    {'id': '1', 'label': 'Goths'},
                    {'id': '1', 'label': 'Huns'},
                    {'id': '1', 'label': 'Incas'},
                    {'id': '1', 'label': 'Indians'},
                    {'id': '1', 'label': 'Italians'},
                    {'id': '1', 'label': 'Japanese'},
                    {'id': '1', 'label': 'Koreans'},
                    {'id': '1', 'label': 'Magyars'},
                    {'id': '1', 'label': 'Mayans'},
                    {'id': '1', 'label': 'Mongols'},
                    {'id': '1', 'label': 'Persians'},
                    {'id': '1', 'label': 'Saracens'},
                    {'id': '1', 'label': 'Slavs'},
                    {'id': '1', 'label': 'Spanish'},
                    {'id': '1', 'label': 'Teutons'},
                    {'id': '1', 'label': 'Turks'},
                    {'id': '3', 'label': 'Vikings'}
                ]
        else:
            obj = [
                     {'id': '1', 'label': 'Test1'},
                     {'id': '2', 'label': 'Test2'},
                     {'id': '3', 'label': 'Test3'}
            ]


        self.response.out.write(json.dumps(obj))


app = webapp2.WSGIApplication([
    webapp2.Route('/api/players/<playerId>', handler=PlayersHandler),
    webapp2.Route('/api/gamesettings/<settingname>', handler=GameTypesHandler)
], debug=True)



