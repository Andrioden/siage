#!/usr/bin/env python

import webapp2
import json
import logging
from models import CivilizationStats, CIVILIZATIONS
from utils import error_400


class CivsHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET CIVLIST DATA --------- """
        self.response.headers['Content-Type'] = 'application/json'
        civs_stats_data = [_get_stats_for_civ(civ) for civ in CIVILIZATIONS]
        self.response.out.write(json.dumps(civs_stats_data))


class CivHandler(webapp2.RequestHandler):
    def get(self, civ_name):
        """ --------- GET SINGLE CIV --------- """
        self.response.headers['Content-Type'] = 'application/json'

        # Validate if actual civ
        if not civ_name in CIVILIZATIONS:
            error_400(self.response, "VALIDATION_ERROR_UNKNOWN_CIV", "The civilization %s is unknown" % civ_name)
            return

        self.response.out.write(json.dumps(_get_stats_for_civ(civ_name)))


def _get_stats_for_civ(civ_name):
        civ_stats = CivilizationStats.query(CivilizationStats.name == civ_name).get()
        if not civ_stats:
            civ_stats = CivilizationStats(name = civ_name)

        civ_stats.calc_and_update_stats_if_needed()

        return civ_stats.get_data()

app = webapp2.WSGIApplication([
    (r'/api/civs/', CivsHandler),
    (r'/api/civs/(\S+)', CivHandler),
], debug=True)