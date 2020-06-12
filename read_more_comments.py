import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from myuser import MyUser
from post import Post
from comment import Comment


# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Read_More_Comments(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # pull the current user from the Request
        user = users.get_current_user()
        ID =self.request.get("ID")
        pID =self.request.get("pID")

        vuser = ""
        myuser = ""
        post_obj = ""

        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', ID)
            myuser = myuser_key.get()

            vuser_key = ndb.Key('MyUser', user.user_id())
            vuser = vuser_key.get()

            post_key = ndb.Key('Post', pID)
            post_obj = post_key.get()


            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id = user.user_id())
                myuser.email_address = user.email()
                myuser.put()

            if not vuser.username:
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            login_status = "You are not logged in."
            url_string = 'login'
            self.redirect('/')



        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'myuser' : myuser,
            'vuser' : vuser,
            'post_obj' : post_obj

        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('read_more_comments.html')
        self.response.write(template.render(template_values))
