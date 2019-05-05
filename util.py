import webapp2
import jinja2
import os
import logging
import datetime
from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from models.myuser import MyUser


def registerUser(username,fname,lname,email,password,birthday,gender,bio):
    userDetails = MyUser(id=username)
    userDetails.fname = fname
    userDetails.lname = lname
    userDetails.username = username
    userDetails.email = email
    userDetails.password = password
    userDetails.birthday = birthday
    userDetails.gender = gender
    userDetails.aboutMe = bio
    userDetails.put()
