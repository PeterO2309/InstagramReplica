import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging
import time
from datetime import datetime

from google.appengine.api.images import get_serving_url


from newpost import uploadPost
from myuser import MyUser
from newpost import NewPost
from comment import Comment
from profile_page import Profile_Page
from search import UserSearch
from fwing import Fwing_Page
from fwers import Fwers_Page
from post import Post
from read_more_comments import Read_More_Comments

# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        myuser = ''
        combined_posts = []
        combined_posts_time = []
        cs = []

        # pull the current user from the Request
        user = users.get_current_user()

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

            #logging.info("# DEBUG: ")
            #print(myuser.key.id())
            #logging.info("End")

            cs.append(myuser)

            for i in myuser.following:
                user_obj = i.get()
                cs.append(user_obj)
                #cs.append(i.get().key)

            #mainpage_timeline = Post.query(Post.)

            for i in cs:
                for m in (i.posts):
                    post_obj = m.get()
                    combined_posts.append(post_obj)
                #for n in (i.get().posts):
                    #combined_posts_time.append(n.get().posting_time)

            #que = Post.query(MyUser.posts.IN(combined_posts)).order(Post.posting_time).fetch()



            logging.info("# DEBUG: ")
            print

        else:
            url = users.create_login_url(self.request.uri)
            login_status = "You are not logged in."
            url_string = 'login'


        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'myuser' : myuser,
            'combined_posts' : combined_posts,
            #'combined_posts' : combined_posts[:50],
            #'combined_posts_time' : combined_posts_time,
            'get_serving_url': get_serving_url,
            #'que' : que,
        }


        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))





    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if (self.request.get('button') == 'Add Username'):
            id =self.request.get("ID")
            #id = long(id)

            myuser_key = ndb.Key('MyUser', id)
            myuser = myuser_key.get()

            username =self.request.get("username")
            myuser.username = username

            myuser.put()
            self.redirect('/')

        elif (self.request.get('button') == 'ADD'):
            id =self.request.get("ID")
            pid =self.request.get("pID")
            hcomment = self.request.get('hcomment')


            myuser_key = ndb.Key('MyUser', id)
            myuser = myuser_key.get()

            post_key = ndb.Key('Post', pid)
            post_obj = post_key.get()

            comment_obj = Comment()
            comment_obj.comment_text = hcomment
            comment_obj.comment_by = myuser.username
            comment_obj.commenter_email = myuser.email_address
            comment_obj.comment_time = datetime.now()

            logging.info("# DEBUG: ")
            #print(comment_obj.comment_text)
            #print(comment_obj.comment_by)
            #print(comment_obj.comment_time)
            logging.info("End")

            comment_obj.put()

            post_obj.comment_k.append(comment_obj.key)
            post_obj.put()
            self.redirect('/')

        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    ('/upload_photo',uploadPost),
    ('/profile_page', Profile_Page),
    ('/search', UserSearch),
    ('/fwing', Fwing_Page),
    ('/fwers', Fwers_Page),
    ('/read_more_comments', Read_More_Comments),

], debug=True)
