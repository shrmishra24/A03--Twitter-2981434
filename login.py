import webapp2
import jinja2
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from models.myuser import MyUser
import urllib2
import urllib
import cookielib

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
class LoginPage(webapp2.RequestHandler):
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
        logging.info('myuser')
        logging.info(user.user_id())
        logging.info(myuser)
        if myuser == None:
            self.redirect('/register')
        else:
            self.redirect('/profile')

    # def post(self):
    #     action = self.request.get('button')
    #     if action == 'Login':
    #         username = self.request.get('username')
    #         password = self.request.get('psw')
    #
    #         query = MyUser.query(MyUser.username == username)
    #         for user in query.fetch(1):
    #             var = True
    #             if user.password == password:
    #                 cj=cookielib.CookieJar()
    #                 opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #                 request=urllib2.Request("http://localhost:8080/profile")
    #                 self.response.set_cookie('userName',username)
    #                 self.redirect('/profile')
    #             else:
    #                 password_chk = password
    #                 logging.info("password_chk "+password_chk)
    #                 rendered_template = {
    #                 'password_chk' : password_chk
    #                 }
    #                 template = JINJA_ENVIRONMENT.get_template('templates/login.html')
    #                 self.response.write(template.render(rendered_template))
    #                 self.redirect('/')
    #     elif action =='Sign Up':
    #         self.redirect('/register')
