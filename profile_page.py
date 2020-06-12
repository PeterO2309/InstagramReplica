import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging


from google.appengine.api.images import get_serving_url
from myuser import MyUser
from comment import Comment
import time
from datetime import datetime


# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

def render_template(template_file, template_values):
    template = JINJA_ENVIRONMENT.get_template(template_file)
    return template.render(template_values)

class Profile_Page(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # pull the current user from the Request
        url = ''
        url_string = ''
        user = users.get_current_user()
        url_ID =self.request.get("url_ID")
        vuser = ""
        myuser = ""
        following = 0
        followers = 0
        cs = []
        combined_posts = []

        # determine if we have a user logged in or not
        if user:
            myuser_key = ndb.Key('MyUser', url_ID)
            myuser = myuser_key.get()

            vuser_key = ndb.Key('MyUser', user.user_id())
            vuser = vuser_key.get()


            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id = user.user_id())
                myuser.email_address = user.email()
                myuser.put()

            #mainpage_timeline = Post.query(Post.)


            if not vuser.username:
                self.redirect('/')

            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            following = len(myuser.following)
            followers = len(myuser.followers)

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
            'get_serving_url': get_serving_url,
            'following' : following,
            'followers' : followers,
            #'combined_posts' : combined_posts[:50],

        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('profile_page.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if (self.request.get('button') == 'Follow'):
            user = users.get_current_user()
            url_ID =self.request.get("url_ID")

            logging.info("# DEBUG: ")
            print(url_ID)
            logging.info("End")

            myuser_key = ndb.Key('MyUser', url_ID)
            myuser = myuser_key.get()

            vuser_key = ndb.Key('MyUser', user.user_id())
            vuser = vuser_key.get()

            myuser.followers.append(vuser_key)
            vuser.following.append(myuser_key)

            myuser.put()
            vuser.put()

            self.redirect('/profile_page?url_ID=' + str(url_ID))

        elif (self.request.get('button') == 'Unfollow'):
            user = users.get_current_user()
            url_ID =self.request.get("url_ID")

            logging.info("# DEBUG: ")
            print(url_ID)
            logging.info("End")

            myuser_key = ndb.Key('MyUser', url_ID)
            myuser = myuser_key.get()

            vuser_key = ndb.Key('MyUser', user.user_id())
            vuser = vuser_key.get()

            myuser.followers.remove(vuser_key)
            vuser.following.remove(myuser_key)

            myuser.put()
            vuser.put()

            self.redirect('/profile_page?url_ID=' + str(url_ID))

        elif (self.request.get('button') == 'ADD'):
            id =self.request.get("ID")
            pid =self.request.get("pID")
            hcomment = self.request.get('hcomment')

            myuser_key = ndb.Key('MyUser', id)
            myuser = myuser_key.get()

            user = users.get_current_user()
            vuser_key = ndb.Key('MyUser', user.user_id())
            vuser = vuser_key.get()

            post_key = ndb.Key('Post', pid)
            post_obj = post_key.get()

            comment_obj = Comment()
            comment_obj.comment_text = hcomment
            comment_obj.comment_by = vuser.username
            comment_obj.commenter_email = vuser.email_address
            comment_obj.comment_time = datetime.now()

            logging.info("# DEBUG: ")
            #print(comment_obj.comment_text)
            #print(comment_obj.comment_by)
            #print(comment_obj.comment_time)
            logging.info("End")

            comment_obj.put()

            post_obj.comment_k.append(comment_obj.key)
            post_obj.put()
            self.redirect('/profile_page?url_ID=' + str(id))
