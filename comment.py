from google.appengine.ext import ndb

class Comment(ndb.Model):
    comment_text = ndb.StringProperty(required=True)
    comment_by = ndb.StringProperty(required=True)
    commenter_email = ndb.StringProperty(required=True)
    comment_time = ndb.DateTimeProperty()
