import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from myuser import MyUser



# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class UserSearch(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'''

        query = MyUser.query()

        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        myuser = ''

        # pull the current user from the Request
        user = users.get_current_user()

        # determine if we have a user logged in or not
        if user:
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id = user.user_id(),)
                myuser.email_address = user.email()
                myuser.put()

            if not myuser.username:
                self.redirect('/')

        else:
            url = users.create_login_url(self.request.uri)
            login_status = "You are not logged in."
            url_string = 'login'
            self.redirect('/')



        template_values = {
            'user' : user,
            'myuser' : myuser,
        }


        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        users_list = []
        users_email_list = []
        #all_users = MyUser.query(ndb.AND(MyUser.email_address != myuser.email_address))


        if (self.request.get('button') == 'Search user'):
            query = MyUser.query()
            query = list(query)


            id =self.request.get("ID")

            myuser_key = ndb.Key('MyUser', id)
            myuser = myuser_key.get()

            username_s =self.request.get("username")

            for i in query:

                if username_s.lower() in i.username.lower():
                    users_list.append(i)
                    #logging.info("# DEBUG: ")
                    #print(users_list)
                    #print(i.username)
                    #print(username_s)
                    #logging.info("End")


            #myuser.put()
            #self.redirect('/')


            template_values = {
                'myuser' : myuser,
                'users_list' : users_list
            }


            # pull the template file and ask jinja to render
            # it with the given template values
            template = JINJA_ENVIRONMENT.get_template('search.html')
            self.response.write(template.render(template_values))
