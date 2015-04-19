#!/usr/bin/env python

import webapp2
import json
import logging
from models import PlayerResult


class CivsHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET CIVLIST DATA --------- """
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(_get_civ_stats()))


class CivHandler(webapp2.RequestHandler):
    def get(self, civ_name):
        """ --------- GET SINGLE CIV --------- """
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(_get_civ_stats(civ_name)))


def _get_civ_stats(civ_filter_name=None):
    # Customize query if only a specific civ should be queried
    player_results = PlayerResult.query()
    if civ_filter_name:
        player_results = player_results.filter(PlayerResult.civilization == civ_filter_name)

    # Get raw data from db
    civs_data = {}
    for res in player_results:
        if not civs_data.has_key(res.civilization):
            civs_data[res.civilization] = {'name': res.civilization, 'played': 0, 'wins': 0}
        civs_data[res.civilization]['played'] += 1
        if res.is_winner:
            civs_data[res.civilization]['wins'] += 1

    # Process data and return it according to single civ or full civ list
    if civ_filter_name:
        civ_data = civs_data[civ_filter_name]
        civ_data['win_chance'] = int(civ_data['wins'] * 100.0 / civ_data['played'])
        return civ_data
    else:
        civs_data_list = []
        for key, civ_dict in civs_data.iteritems():
            civ_dict['win_chance'] = int(civ_dict['wins'] * 100.0 / civ_dict['played'])
            civs_data_list.append(civ_dict)
        return civs_data_list


app = webapp2.WSGIApplication([
    (r'/api/civs/', CivsHandler),
    (r'/api/civs/(\S+)', CivHandler),
], debug=True)