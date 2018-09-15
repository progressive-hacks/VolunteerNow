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


class Event(ndb.Model):
    user = ndb.StringProperty();
    eventName = ndb.StringProperty();
    start_time = ndb.DateTimeProperty();
    end_time = ndb.DateTimeProperty();
    description = ndb.TextProperty();
    # geolocation = ndb.GeoPtProperty()
# ________________________________________________________________________________
# Autumn's comment: We need a organizer handler so that information can be
# entered into the ndb database, then retrieved from it when the calendar page loads
# ________________________________________________________________________________

class HomePage(webapp2.RequestHandler):

    def get(self):
        content = JINJA_ENV.get_template('templates/homepage.html')
        user = users.get_current_user()
        if user:
            start_link = "/volunteer"
        else:
            start_link = users.create_login_url('/volunteer')

        self.response.write(content.render(content=start_link))

class VolunteerHandler(webapp2.RequestHandler):
    def get(self):
        content = JINJA_ENV.get_template("templates/divsForCalendar.html")
        logout = users.create_logout_url('/')

        self.response.write(content.render(logout=logout))

    def post(self):
        pass

class OrganizerHandler(webapp2.RequestHandler):
    def get(self):
        content = JINJA_ENV.get_template("templates/organizer.html")
        self.response.write(content.render())

    def post(self):
        user = users.get_current_user().user_id()
        eventName = self.request.get('eventName')
        start_time = self.request.get('start_time')
        end_time = self.request.get('end_time')
        description = self.request.get('description')

        print(start_time, end_time)

        EventData = Event(user = user, eventName = eventName, 
            end_time = helpers.create_datetime(end_time), 
            start_time = helpers.create_datetime(start_time),
            description = description)
        
        EventData.put()
        #self.redirect('/volunteer')


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/volunteer', VolunteerHandler),
    ('/organizer', OrganizerHandler)
], debug=True)
