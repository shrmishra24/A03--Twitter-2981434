import webapp2
import jinja2
import os
import base64
import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from models.myuser import MyUser
from models.twitterContent import Content
import cookielib
import urllib2
import mimetypes
import datetime
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class TweetSearchPage(webapp2.RequestHandler):
    tweetContent = ""
    def get(self):
        tweetToSearch=self.request.cookies.get('tweetSearchInput')
        tweetToSearch.lower()

        tweetSearched=['']
        content = Content.query().fetch()
        for x in content:
            if tweetToSearch in x.tweetContent.lower():
                tweetSearched.append(x.tweetContent)

        results_dict = {'logout_url' : users.create_logout_url('/'),
                        'tweetSearched' : tweetSearched
                        }

        template = JINJA_ENVIRONMENT.get_template('templates/tweetSearch.html')
        self.response.write(template.render(results_dict))
        return
