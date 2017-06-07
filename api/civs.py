#!/usr/bin/env python

import webapp2
import json
import logging
from models import CivilizationStats, CIVILIZATIONS
from utils import *


class CivsHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET CIVLIST DATA --------- """
        civs_stats_data = [_get_stats_for_civ(civ) for civ in CIVILIZATIONS]
        set_json_response(self.response, civs_stats_data)


class CivHandler(webapp2.RequestHandler):
    def get(self, civ_name):
        """ --------- GET SINGLE CIV --------- """

        # Validate if actual civ
        if civ_name not in CIVILIZATIONS:
            error(400, self.response, "VALIDATION_ERROR_UNKNOWN_CIV", "The civilization %s is unknown" % civ_name)
            return

        set_json_response(self.response, _get_stats_for_civ(civ_name))


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