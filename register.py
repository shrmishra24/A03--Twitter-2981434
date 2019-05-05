import webapp2
import jinja2
import os
import logging
import datetime
from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from models.myuser import MyUser
import util
import cookielib
import urllib2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class RegisterPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/register.html')
        self.response.write(template.render())
        return

    def post(self):
        action = self.request.get('button')
        if action == 'register':
            user = users.get_current_user()

            fname = self.request.get('fname')
            lname = self.request.get('lname')
            email = self.request.get('email')
            username = self.request.get('username')
            password = self.request.get('psw')
            gender = self.request.get('gender')
            birthday = datetime.strptime(self.request.get('birthday'), '%Y-%m-%d')
            bio = self.request.get('bio')

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            logging.info(myuser_key)
            # Saving into myuser
            userDetails = MyUser(id=user.user_id())
            userDetails.fname = fname
            userDetails.lname = lname
            userDetails.username = username
            userDetails.email = email
            userDetails.password = password
            userDetails.birthday = birthday
            userDetails.gender = gender
            userDetails.aboutMe = bio
            userDetails.put()

        #    util.registerUser(username,fname,lname,email,password,birthday,gender,bio)

            cj=cookielib.CookieJar()
            opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            request=urllib2.Request("http://localhost:8080/profile")
            self.response.set_cookie('userName',username)

            self.redirect('/profile')
