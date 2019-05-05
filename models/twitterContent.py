from google.appengine.ext import ndb

class Content(ndb.Model):
    # profile_id = ndb.StringProperty()
    tweetContent = ndb.StringProperty(indexed=False)
    date = ndb.DateProperty(auto_now_add=True)
    image_file = ndb.StringProperty()
    image = ndb.BlobProperty()
