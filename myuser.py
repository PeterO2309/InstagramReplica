from google.appengine.ext import ndb

from post import Post



class MyUser(ndb.Model):
    # email address of this user
    email_address = ndb.StringProperty()
    username = ndb.StringProperty()
    following = ndb.KeyProperty(repeated=True)
    followers = ndb.KeyProperty(repeated=True)
    posts = ndb.KeyProperty(kind = Post, repeated=True)
