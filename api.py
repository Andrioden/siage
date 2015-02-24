#!/usr/bin/env python

import webapp2
import json

class PlayersListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = [
            {'nickname': 'Andrioden', 'rating': 1670, 'winrate': '55', 'bestcivilization': 'Huns'},
            {'nickname': 'Shrubber', 'rating': 1614, 'winrate': '51', 'bestcivilization': 'Mongols'}
        ]
        self.response.out.write(json.dumps(obj))

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write("POST (Save) received with data: " + self.request.body)

class PlayerHandler(webapp2.RequestHandler):
    def get(self, playerId):
        self.response.headers['Content-Type'] = 'application/json'
        obj = [
            {'nickname': 'Andrioden', 'rating': 1670, 'winrate': '55', 'bestcivilization': 'Huns'}
        ]
        self.response.out.write(json.dumps(obj))

    def put(self, playerId):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write("PUT (Update) received with data: " + self.request.body)

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
    webapp2.Route(r'/api/players/', handler=PlayersListHandler, name='players'),
    webapp2.Route(r'/api/players/<playerId:(\d+)>', handler=PlayerHandler, name='player'),
    webapp2.Route(r'/api/gamesettings/<settingname>', handler=GameTypesHandler, name='gamesetting')
], debug=True)



"""
\d	Any digit, short for [0-9]
\D	A non-digit, short for [^0-9]
\s	A whitespace character, short for [ \t\n\x0b\r\f]
\S	A non-whitespace character, short for [^\s]
\w	A word character, short for [a-zA-Z_0-9]
\W	A non-word character [^\w]
\S+	Several non-whitespace characters
\b	Matches a word boundary where a word character is [a-zA-Z0-9_].
"""