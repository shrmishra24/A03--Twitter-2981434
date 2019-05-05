import webapp2
from webapp2 import Route

app = webapp2.WSGIApplication([
    Route('/', handler = 'login.LoginPage'),
    Route('/register', handler = 'register.RegisterPage'),
    Route('/profile', handler = 'profile.ProfilePage'),
    Route('/view', handler = 'view.ViewPage'),
    Route('/tweetSearch', handler = 'tweetSearch.TweetSearchPage'),
    Route('/followingTweets', handler = 'followingTweets.FollowingTweets'),
],debug=True)
