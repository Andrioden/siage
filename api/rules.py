#!/usr/bin/env python

import webapp2
import json
import logging
from models import Rule
from utils import validate_authenticated, validate_logged_in_admin

class RulesHandler(webapp2.RequestHandler):
    def get(self):
        """ --------- GET RULES --------- """
        data = [rule.get_data() for rule in Rule.query()]
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))

    def post(self):
        """ --------- CREATE RULE --------- """

        # VALIDATING
        if not validate_authenticated(self.response):
            return

        # PROCESS REQUEST
        new_rule = Rule(name = self.request.get('name'), description = self.request.get('description')).put()

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(new_rule.get().get_data()))

class RuleHandler(webapp2.RequestHandler):
    def put(self, rule_id):
        """ --------- UPDATE RULE --------- """

        # VALIDATING
        if not validate_authenticated(self.response):
            return

        # PROCESS REQUEST
        rule = Rule.get_by_id(int(rule_id))
        rule.name = self.request.get('name')
        rule.description = self.request.get('description')
        rule.put()

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(rule.get_data()))

    def delete(self, rule_id):
        """ --------- DELETE RULE --------- """

        # VALIDATING
        if not validate_logged_in_admin(self.response):
            return

        # PROCESS REQUEST
        Rule.get_by_id(int(rule_id)).key.delete()

        # RETURN RESPONSE
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'response': "success", 'rule_id': rule_id}))

app = webapp2.WSGIApplication([
    (r'/api/rules/', RulesHandler),
    (r'/api/rules/(\d+)', RuleHandler),
], debug=True)