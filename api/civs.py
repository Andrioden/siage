#!/usr/bin/env python

import webapp2
import json
import logging
from models import PlayerResult

class CivsHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET CIVLIST DATA --------- """
        # BUILD DATA
        civs_data = {}
        for res in PlayerResult.query():
            if not civs_data.has_key(res.civilization):
                civs_data[res.civilization] = {'name': res.civilization, 'played': 0, 'wins': 0}
            civs_data[res.civilization]['played'] += 1
            if res.is_winner:
                civs_data[res.civilization]['wins'] += 1
        
        civs_data_list = []
        for key, civ_dict in civs_data.iteritems():
            civ_dict['win_chance'] = int(civ_dict['wins'] * 100.0 / civ_dict['played'])
            civs_data_list.append(civ_dict)
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(civs_data_list))

class CivHandler(webapp2.RequestHandler):
    def get(self, civ_name):
        """ --------- GET SINGLE CIV --------- """
        
        civ_data = {'name': civ_name, 'played': 0, 'wins': 0}
        for res in PlayerResult.query(PlayerResult.civilization == civ_name):
            civ_data['played'] += 1
            if res.is_winner:
                civ_data['wins'] += 1
        
        civ_data['win_chance'] = int(civ_data['wins'] * 100.0 / civ_data['played'])
        
        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(civ_data))

app = webapp2.WSGIApplication([
    (r'/api/civs/', CivsHandler),
    (r'/api/civs/(\S+)', CivHandler),
], debug=True)