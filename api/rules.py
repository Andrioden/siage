#!/usr/bin/env python

import webapp2
import json
import logging
from models import Rule, Game
from utils import validate_authenticated, validate_logged_in_admin
from google.appengine.ext import ndb
from api.utils import error_400

class RulesHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET RULES --------- """
        data = [rule.get_data() for rule in Rule.query()]
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))

    def post(self):
        """ --------- CREATE RULE --------- """
        request_data = json.loads(self.request.body)

        # VALIDATING
        if not validate_authenticated(self.response):
            return

        # PROCESS REQUEST

        new_rule_key = Rule(name = request_data['name'], description = request_data['description']).put()

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(new_rule_key.get().get_data()))

class RuleHandler(webapp2.RequestHandler):
    def put(self, rule_id):
        """ --------- UPDATE RULE --------- """
        request_data = json.loads(self.request.body)

        # VALIDATING
        if not validate_authenticated(self.response):
            return

        # PROCESS REQUEST
        rule = Rule.get_by_id(int(rule_id))
        rule.name = request_data['name']
        rule.description = request_data['description']
        rule.put()

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(rule.get_data()))

    def delete(self, rule_id):
        """ --------- DELETE RULE --------- """

        # VALIDATING
        if not validate_logged_in_admin(self.response):
            return
        elif not self._validate_rule_not_in_use(rule_id):
            return

        # PROCESS REQUEST
        Rule.get_by_id(int(rule_id)).key.delete()

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "success", 'rule_id': rule_id}))

    def _validate_rule_not_in_use(self, rule_id):
        if Game.query(Game.rule == ndb.Key(Rule, int(rule_id))).count() > 0:
            error_400(self.response, "VALIDATION_ERROR_RULE_IN_USE", "The rule you tried to delete is used in a game. It should not be deleted.")
            return False
        else:
            return True

app = webapp2.WSGIApplication([
    (r'/api/rules/', RulesHandler),
    (r'/api/rules/(\d+)', RuleHandler),
], debug=True)