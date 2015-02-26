#!/usr/bin/env python

import webapp2
import json
from models import Player

class PlayersListHandler(webapp2.RequestHandler):
    def get(self):
        # BUILD DATA
        players_data = []
        for player in Player().query():
            players_data.append(player.get_data())
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(players_data))

    def post(self):
        # PROCESS REQUEST
        data = json.loads(self.request.body)
        Player(nick = data['nick']).put()
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("POST (Save) received with data: " + self.request.body)

class PlayerHandler(webapp2.RequestHandler):
    def get(self, playerId):
        # BUILD DATA
        print "Finding player"
        player_data = Player.get_by_id() 
        
        self.response.headers['Content-Type'] = 'application/json'
        obj = [
            {'nickname': 'Andrioden', 'rating': 1670, 'winrate': '55', 'bestcivilization': 'Huns'}
        ]
        self.response.out.write(json.dumps(obj))

    def put(self, playerId):
        self.response.headers['Content-Type'] = 'application/text'
        self.response.out.write("PUT (Update) received with data: " + self.request.body)

app = webapp2.WSGIApplication([
    webapp2.Route(r'/api/players/', handler=PlayersListHandler, name='players'),
    webapp2.Route(r'/api/players/<playerId:(\d+)>', handler=PlayerHandler, name='player'),
], debug=True)