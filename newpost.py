import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


from datetime import datetime
from myuser import MyUser
from post import Post


# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class NewPost(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        myuser = ''

        # pull the current user from the Request
        user = users.get_current_user()

        upload_url = blobstore.create_upload_url('/upload_photo')

        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id = user.user_id(),)
                myuser.email_address = user.email()
                myuser.put()

            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            if not myuser.username:
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            self.redirect('/')


        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'myuser' : myuser,
            'upload_url' : upload_url,
        }


            # pull the template file and ask jinja to render
            # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('newpost.html')
        self.response.write(template.render(template_values))

class uploadPost(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key(MyUser, user.user_id())
        myuser = myuser_key.get()

        if (self.request.get('button') == 'Add Image'):
            h_caption = self.request.get('caption')
            upload = self.get_uploads()[0]
            blobinfo = blobstore.BlobInfo(upload.key())

            #datetime_obj = datetime.now()

            post_obj = Post()
            post_obj.image = upload.key()
            post_obj.caption = h_caption
            post_obj.creator = myuser.email_address
            post_obj.posting_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            post_obj.key = ndb.Key('Post', str(upload.key()))

            postkey = post_obj.put()

            logging.info("DEBUG")
            #print(postkey)
            logging.info("END")

            myuser.posts.append(post_obj.key)
            myuser.put()

            self.redirect('/')
