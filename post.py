from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore

from comment import Comment


class Post(ndb.Model):
    caption = ndb.StringProperty()
    image = ndb.BlobKeyProperty(required=True)
    creator = ndb.StringProperty()
    posting_time = ndb.StringProperty()
    comment_k = ndb.KeyProperty(kind = Comment, repeated = True)
