from google.appengine.ext import ndb

class Player(ndb.Model):
    nick = ndb.StringProperty()