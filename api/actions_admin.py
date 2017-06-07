#!/usr/bin/env python

import webapp2
import json
from google.appengine.ext import ndb
from google.appengine.ext import deferred
from rating import recalculate_ratings
from models import *
from api.utils import validate_logged_in_admin
import logging
from utils import *


class ReCalcRatingHandler(webapp2.RequestHandler):
    def post(self):
        if not validate_logged_in_admin(self.response):
            return

        deferred.defer(recalculate_ratings)

        set_json_response(self.response, {'response': "Ratings recalculation started and will take more than 60 seconds."})


class FixDBHandler(webapp2.RequestHandler):
    def post(self):
        """ This admin function will contain all historic and current clean up method.
        Please uncomment them when they are run on prod

        """

        if not validate_logged_in_admin(self.response):
            return

        # logging.info("----- 01.04.2015 - PlayerResult: removing next_player_result  ------")
        # for res in PlayerResult.query():
        #     if 'next_player_result' in res._properties:
        #         del res._properties['next_player_result']
        #     res.game_date = res.game.get().date
        #     res.put()
        #
        # logging.info("----- 01.04.2015 - Player: removing some stats best/worst properties  ------")
        # for player in Player.query():
        #     self._delete_property(player, 'stats_best_civ')
        #     self._delete_property(player, 'stats_best_civ_wins')
        #     self._delete_property(player, 'stats_worst_civ')
        #     self._delete_property(player, 'stats_worst_civ_losses')
        #     self._delete_property(player, 'stats_civ_most_wins_name')
        #     self._delete_property(player, 'stats_civ_most_wins_count')
        #     self._delete_property(player, 'stats_civ_most_losses_name')
        #     self._delete_property(player, 'stats_civ_most_losses_count')
        #     player.put()
        # logging.info("----- 10.09.2015 - Game: Renamed victory Standad to Standard  ------")
        # for game in Game.query(Game.victory == "Standad"):
        #     game.victory = "Standard"
        #     game.put()
        # logging.info("----- 10.09.2015 - Player: Set all players to active ------")
        # for player in Player.query():
        #     player.active = True
        #     player.put()

        set_json_response(self.response, {'response': "The database has been cleaned"})

    def _delete_property(self, obj, property_name):
        if property_name in obj._properties:
            del obj._properties[property_name]


class ClearStatsHandler(webapp2.RequestHandler):
    def post(self):

        if not validate_logged_in_admin(self.response):
            return

        for player in Player.query():
            player.clear_stats()
        ndb.delete_multi(CivilizationStats.query().fetch(keys_only=True))

        set_json_response(self.response, {'response': "Player statistics have been cleared"})


class AdjustRatingHandler(webapp2.RequestHandler):
    def post(self):

        if not validate_logged_in_admin(self.response):
            return

        request_data = json.loads(self.request.body)
        player_id = request_data['player_id']
        new_rating_adjustment = request_data['new_rating_adjustment']

        player = Player.get_by_id(int(player_id))
        player.set_new_rating_adjustment(new_rating_adjustment)

        set_json_response(self.response, {'response': "%s now has an rating adjustment at %s. Remember to recalculate ratings if player have been part of games." % (player.nick, new_rating_adjustment)})


class ResetRatingAdjustment(webapp2.RequestHandler):
    def post(self):

        if not validate_logged_in_admin(self.response):
            return

        for player in Player.query().fetch():
            player.rating_adjustment = 0
            player.put()

        set_json_response(self.response, {'response': "Rating adjustment reset. Remember to recalculate ratings if player have been part of games."})


class DataImportPythonScript(webapp2.RequestHandler):
    def get(self):

        if not validate_logged_in_admin(self.response):
            return

        self.response.out.write("# FULL PYTHON SCRIPT: <br/>")
        self.response.out.write("<br/>")
        self.response.out.write("# IMPORTS: <br/>")
        self.response.out.write("from models import * <br/>")
        self.response.out.write("from datetime import datetime <br/>")
        self.response.out.write("from google.appengine.ext import ndb <br/>")
        self.response.out.write("<br/>")
        self.response.out.write("# CLEAR DB: <br/>")
        self.response.out.write("ndb.delete_multi(Player.query().fetch(keys_only=True)) <br/>")
        self.response.out.write("ndb.delete_multi(Rule.query().fetch(keys_only=True)) <br/>")
        self.response.out.write("ndb.delete_multi(Game.query().fetch(keys_only=True)) <br/>")
        self.response.out.write("ndb.delete_multi(PlayerResult.query().fetch(keys_only=True)) <br/>")
        self.response.out.write("<br/>")
        self.response.out.write("# PLAYERS: <br/>")
        for player in Player.query().fetch():
            self.response.out.write(self._get_data_dump_string_of_object(player) + "<br><br>")
        self.response.out.write("<br/>")
        self.response.out.write("# RULES: <br/>")
        for rule in Rule.query().fetch():
            self.response.out.write(self._get_data_dump_string_of_object(rule) + "<br><br>")
        self.response.out.write("<br/>")
        self.response.out.write("# GAMES: <br/>")
        for game in Game.query().fetch():
            self.response.out.write(self._get_data_dump_string_of_object(game) + "<br><br>")
        self.response.out.write("<br/>")
        self.response.out.write("# PlayerResults: <br/>")
        for player_result in PlayerResult.query().fetch():
            self.response.out.write(self._get_data_dump_string_of_object(player_result) + "<br><br>")

        # Uncomment below to download as file, not really practical but keeping code
        #self.response.headers['Content-Type'] = 'text/csv'
        #self.response.headers['Content-Disposition'] = "attachment; filename=siage_import_script.py"


    def _get_data_dump_string_of_object(self, obj):
        data_string = "%s(id=%s, " % (type(obj).__name__, obj.key.id())
        for variable_name in obj.__dict__['_values'].keys():  # __dict__['_values'] contains all class object variables
            variable_value = getattr(obj, variable_name, None)
            if variable_name == "is_host":
                continue
            elif variable_value is None:
                data_string += "%s=None, " % variable_name
            elif type(variable_value) is list:
                continue
            elif type(variable_value) in (int, long, bool, float):
                data_string += "%s=%s, " % (variable_name, variable_value)
            elif type(variable_value) is unicode:
                escaped_value = variable_value.replace("\'", "\\'").replace("\"", "\\\"")
                data_string += "%s='%s', " % (variable_name, escaped_value)
            elif type(variable_value) is datetime:
                data_string += "%s=datetime.fromtimestamp(%s), " % (variable_name, date_to_epoch(variable_value))
            elif type(variable_value) is ndb.Key:
                data_string += "%s=ndb.Key(%s, %s), " % (variable_name, variable_value.kind(), variable_value.id())
            else:
                raise Exception("Type not handled: " + type(variable_value).__name__)

        data_string = data_string[:-2]
        data_string += ").put()"
        return data_string

app = webapp2.WSGIApplication([
    (r'/api/actions/admin/recalcrating/', ReCalcRatingHandler),
    (r'/api/actions/admin/fixdb/', FixDBHandler),
    (r'/api/actions/admin/clearstats/', ClearStatsHandler),
    (r'/api/actions/admin/adjustrating/', AdjustRatingHandler),
    (r'/api/actions/admin/resetratingadjustment/', ResetRatingAdjustment),
    (r'/api/actions/admin/dataimportpythonscript/', DataImportPythonScript),
], debug=True)
