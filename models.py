from google.appengine.ext import ndb

class Player(ndb.Model):
    nick = ndb.StringProperty()
    
    def get_data(self):
        return {'id': self.key.id(), 'nick': self.nick}