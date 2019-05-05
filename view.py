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
class ViewPage(webapp2.RequestHandler):
    tweetContent = ""
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        userSearchName=self.request.cookies.get('userSearchName')
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
        loggedinUser = myuser.username

        userDetails = MyUser.query(MyUser.username == userSearchName).fetch()
        userSearched = ''
        for x in userDetails:
            userSearched = x.key

        logging.info("user searched ")
        logging.info(userSearched)

        if userSearched == '':
            results_dict = {'logout_url' : users.create_logout_url(self.request.uri),
                            'notExist' : 'User does not exist'
                            }
            template = JINJA_ENVIRONMENT.get_template('templates/view.html')
            self.response.write(template.render(results_dict))
            return
        else:

            myuser = userSearched.get()  # to get the key of the searched user
            countFollower =0;
            countFollowing = 0;

            if loggedinUser == userSearchName:
                self.redirect('/profile')

            else:
                for x in myuser.followFollowingList:
                    if x.followers:
                        countFollower = countFollower+1
                    if x.following:
                        countFollowing = countFollowing+1
                logging.info(myuser.myuserTweet.reverse())
                results_dict = {'logout_url' : users.create_logout_url('/'),
                                'userDetails' : userDetails,
                                'twt' : myuser.myuserTweet,
                                'myuser' : myuser,
                                'username' : loggedinUser,
                                'listFollow' : myuser.followFollowingList,
                                'countFollower':countFollower,
                                'countFollowing':countFollowing,
                                'userSearchName' :userSearchName
                                }
                template = JINJA_ENVIRONMENT.get_template('templates/view.html')
                self.response.write(template.render(results_dict))
                return

    def post(self):
        action = self.request.get('button')
        if action == "follow":

            usertoFollow = self.request.cookies.get('userSearchName') #User being searched
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            userFollowing = myuser.username #user who has logged in and searched other user to follow
            logging.info("following and follow users are")
            logging.info(usertoFollow)  #shreya
            logging.info(userFollowing) #shweta


            follower = UserActions(following=usertoFollow)
            follower.put()
            myuser.followFollowingList.append(follower)
            myuser.put()


            #Adding the user whom following
            userDetails = MyUser.query(MyUser.username == usertoFollow).fetch()
            userSearched = ''
            for x in userDetails:
                userSearched = x.key
            myuser = userSearched.get()
            following = UserActions(followers=userFollowing)
            following.put()
            myuser.followFollowingList.append(following)
            myuser.put()
            self.redirect('/view')

        elif action =='unfollow':
            userFollower=self.request.cookies.get('userSearchName')
            userDetails = MyUser.query(MyUser.username == userFollower).fetch()
            userSearched = ''
            for x in userDetails:
                userSearched = x.key
            myuserFollower = userSearched.get()

            user = users.get_current_user()
            myuserFollowing_key = ndb.Key('MyUser', user.user_id())
            myuserFollowing = myuserFollowing_key.get()
            userFollowing = myuserFollowing.username

            myuserFollowing.followFollowingList = [i for i in myuserFollowing.followFollowingList
                                                        if i.following != userFollower]
            myuserFollowing.put()

            myuserFollower.followFollowingList = [i for i in myuserFollower.followFollowingList
                                                        if i.followers != userFollowing]
            myuserFollower.put()
            self.redirect('/view')
