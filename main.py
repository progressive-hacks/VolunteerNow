import os
import webapp2
import jinja2
import helpers

from google.appengine.api import users
from google.appengine.ext import ndb


JINJA_ENV = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

"""
class Event(ndb.Model):
    user = ndb.StringProperty()
    name = ndb.StringProperty()
    start_time = ndb.DateTimeProperty()
    end_time = ndb.DateTimeProperty()
    description = ndb.TextProperty()
    geolocation = ndb.GeoPtProperty()
"""

class HomePage(webapp2.RequestHandler):
    
    def get(self):
        content = JINJA_ENV.get_template('templates/homepage.html')
        user = users.get_current_user()
        if user:
            start_link = "/volunteer"
        else:
            start_link = users.create_login_url('/volunteer')

        self.response.write(content.render(content=start_link))

class CalenderView(webapp2.RequestHandler):

    def get(self):
        content = JINJA_ENV.get_template("templates/divsForCalendar.html")
        self.response.write(content.render())


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/volunteer', CalenderView)
], debug=True)
