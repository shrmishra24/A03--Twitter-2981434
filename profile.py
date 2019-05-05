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
class ProfilePage(webapp2.RequestHandler):
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

        userDetails = MyUser.query(MyUser.username == username).fetch()

        countFollower =0;
        countFollowing = 0;

        for x in myuser.followFollowingList:
            if x.followers:
                countFollower = countFollower+1
            if x.following:
                countFollowing = countFollowing+1

        logging.info(myuser.myuserTweet.reverse())
        results_dict = {'logout_url' : users.create_logout_url(self.request.uri),
                        'userDetails' : userDetails,
                        'twt' : myuser.myuserTweet,
                        'myuser' : myuser,
                        'listFollow' : myuser.followFollowingList,
                        'length' : len(myuser.followFollowingList),
                        'countFollower':countFollower,
                        'countFollowing':countFollowing
                        }

        template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
        self.response.write(template.render(results_dict))
        return

    def post(self):
        action = self.request.get('button')
        user = users.get_current_user()
        if action == 'tweet':
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            username=myuser.username

            tweetContent = self.request.get('tweetContent')
            file_upload = self.request.POST.get("file", None)
            logging.info("file_upload")
            logging.info(file_upload)

            if file_upload!='':
                image_file = file_upload.filename
                image_decode = file_upload.file.read()  # Encoding the string which is coming as an input into image

                tweets = Content(tweetContent=tweetContent,image_file=image_file,image = base64.b64encode(image_decode))
                tweets.put()
            else:
                tweets = Content(tweetContent=tweetContent)
                tweets.put()

            myuser.myuserTweet.append(tweets)
            myuser.put()
            self.redirect('/profile')

        elif action == 'Edit':

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            username=myuser.username

            myuser.fname = self.request.get('fname')
            myuser.lname = self.request.get('lname')
            myuser.email = self.request.get('email')
            myuser.password = self.request.get('psw')
            myuser.aboutMe = self.request.get('aboutMe')
            myuser.birthday = datetime.strptime(self.request.get('birthday'), '%Y-%m-%d')

            myuser.put()
            self.redirect('/profile')

        elif action =='change':
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            username=myuser.username

            picture = self.request.POST.get("pictureName", None)
            filename = picture.filename
            profile_picture = picture.file.read()

            myuser.picture_file = filename
            myuser.profile_picture = base64.b64encode(profile_picture)
            myuser.put()
            self.redirect('/profile')
            # self.redirect('/view')
        elif action =='delete':
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            username=myuser.username

            tweetContent = self.request.get('tweetContent')
            image_file = self.request.get('image_file')
            self.redirect('/profile')
            # tweet_key = ndb.Key('Content', tweetContent)
            # tweetC = tweet_key.get()

            if tweetContent!='':
                myuser.myuserTweet = [i for i in myuser.myuserTweet if i.tweetContent != tweetContent]
                myuser.put()
            elif image_file !='':
                myuser.myuserTweet = [i for i in myuser.myuserTweet if i.image_file != image_file]
                myuser.put()
            elif image_file !='' and tweetContent =='':
                myuser.myuserTweet = [i for i in myuser.myuserTweet if i.image_file != image_file]
                myuser.put()
            else:
                myuser.myuserTweet = [i for i in myuser.myuserTweet if i.tweetContent != tweetContent]
                myuser.put()
                self.redirect('/profile')
            # tweetC.key.delete()

        elif action == "update":
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            username=myuser.username
            tweetContent = self.request.get('tweetContent')
            editedPost = self.request.get('editedPost')
            for post in myuser.myuserTweet:
                if post.tweetContent == tweetContent:
                    post.tweetContent = editedPost
                    logging.info("edited post is: "+editedPost)
                    logging.info("edited post is: "+post.tweetContent)
            myuser.put()
            self.redirect('/profile')

        elif action =="searchUser":
            username = self.request.get("userSearch")
            cj=cookielib.CookieJar()
            opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            request=urllib2.Request("http://localhost:8080/view")
            self.response.set_cookie('userSearchName',username)
            self.redirect('/view')

        elif action == "searchTweet":
            tweetSearch = self.request.get("tweetSearch")
            cj=cookielib.CookieJar()
            opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            request=urllib2.Request("http://localhost:8080/tweetSearch")
            self.response.set_cookie('tweetSearchInput',tweetSearch)
            self.redirect('/tweetSearch')

        elif action == "timeline":
            self.redirect('/followingTweets')
