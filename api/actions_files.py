#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from utils import *
from models import GameFile, Game
import logging


class UploadGameFileUrlHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/api/actions/files/uploadgamefile/')
        set_json_response(self.response, {'upload_url': upload_url})


class UploadGameFileHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        
        if not validate_authenticated(self.response):
            return

        game_id = self.request.get('game_id', None)
        upload = self.get_uploads()[0]

        try:
            if game_id is None:
                raise Exception("Missing game_id input, value is: %s" % game_id)

            game_file = GameFile(
                game=ndb.Key(Game, int(game_id)),
                uploader=current_user_player().key,
                blob=upload.key()
            ).put().get()

            set_json_response(self.response, {'file': game_file.get_data()})
        except Exception, e:
            logging.error("Failed to upload game file. Deleting blob. Exception: %s" % e)
            blobstore.delete(upload.key())


class DeleteGameFileHandler(webapp2.RequestHandler):
    def post(self): # It is post because this allows us to get request data from the request body like every where else
        request_data = json.loads(self.request.body)

        if not validate_logged_in_admin(self.response):
            return
        if not validate_request_data(self.response, request_data, ['game_file_id']):
            return

        game_file = ndb.Key(GameFile, int(request_data['game_file_id'])).get()
        blobstore.delete(game_file.blob)
        game_file.key.delete()

        set_json_response(self.response, {'response': "GameFile deleted."})


class ViewHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, blob_key):
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blob_key)


app = webapp2.WSGIApplication([
    (r'/api/actions/files/uploadgamefileurl/', UploadGameFileUrlHandler),
    (r'/api/actions/files/uploadgamefile/', UploadGameFileHandler),
    (r'/api/actions/files/deletegamefile/', DeleteGameFileHandler),
    (r'/api/actions/files/view/([^/]+)?', ViewHandler),
], debug=True)
