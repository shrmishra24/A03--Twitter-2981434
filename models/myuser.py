from google.appengine.ext import ndb
from twitterContent import Content
from userActions import UserActions
class MyUser(ndb.Model):
    fname = ndb.StringProperty(required = True)
    lname = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True,repeated = False)
    email = ndb.StringProperty(required = True,repeated = False)
    password = ndb.StringProperty(required = True)
    aboutMe = ndb.StringProperty(indexed=False)
    birthday = ndb.DateProperty(required = True)
    gender = ndb.StringProperty(required = True)
    picture_file = ndb.StringProperty()
    profile_picture = ndb.BlobProperty()
    myuserTweet = ndb.StructuredProperty(Content, repeated=True)
    followFollowingList = ndb.StructuredProperty(UserActions, repeated=True)
