import webapp2
import jinja2
import os
import base64
import logging
import cookielib
import urllib2
import mimetypes
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users
from models.myuser import MyUser
from models.twitterContent import Content
from models.userActions import UserActions
from datetime import datetime


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class FollowingTweets(webapp2.RequestHandler):
    tweetContent = ""
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('templates/login.html')
            self.response.write(template.render(template_values))
            return
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        username = myuser.username

        followingUser = []
        tweetsFetched = []
        # userSearchedDetails=[]

        for x in myuser.followFollowingList:
            if x.following:
                followingUser.append(x.following)
                logging.info('followingUser')
                logging.info(followingUser)
        userSearchedDetails = MyUser.query().filter(MyUser.username.IN(followingUser)).fetch()
        for x in userSearchedDetails:
            logging.info(x.myuserTweet)
            x.myuserTweet.reverse()
            results_dict = {'logout_url' : users.create_logout_url('/'),
                            'tweetsFetched' : userSearchedDetails
                            }
        template = JINJA_ENVIRONMENT.get_template('templates/followingTweets.html')
        self.response.write(template.render(results_dict))
