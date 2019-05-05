from google.appengine.ext import ndb

class UserActions(ndb.Model):
    # profile_id = ndb.StringProperty()
    followers = ndb.StringProperty(repeated = False)
    following = ndb.StringProperty(repeated = False)
