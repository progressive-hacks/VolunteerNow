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
    organizer = ndb.StringProperty()
    volunteer = ndb.StringProperty(repeated=True)
    event_name = ndb.StringProperty()
    start_time = ndb.DateTimeProperty()
    final_time = ndb.DateTimeProperty()
    description = ndb.TextProperty()

    # geolocation = ndb.GeoPtProperty()

"""
________________________________________________________
Autumn's comment: We need a organizer handler so that 
information can be entered into the ndb database, then 
retrieved from it when the calendar page loads
________________________________________________________

"""

class HomePage(webapp2.RequestHandler):


    def get(self):
        content = JINJA_ENV.get_template('templates/frontpage.html')
        user = users.get_current_user()
        if user:
            start_link = "/volunteer"
        else:
            start_link = users.create_login_url('/volunteer')

        self.response.write(content.render(content=start_link))

class OrganizerHandler(webapp2.RequestHandler):

    def get(self):
        content = JINJA_ENV.get_template("templates/organizer.html")

        events = Event.query(Event.organizer 
                == users.get_current_user()).order(Event.start_time)

        self.response.write(content.render(events = events))

    def post(self):
        start_time = self.request.get('start_time')
        final_time = self.request.get('final_time')

        event = Event(
            organizer = users.get_current_user(),
            volunteer = [],
            event_name = self.request.get('event_name'),
            start_time = helpers.create_datetime(start_time),
            final_time = helpers.create_datetime(final_time),
            description = self.request.get('description')
        )

        event.put()
        self.redirect('/organizer')

class VolunteerHandler(webapp2.RequestHandler):
    
    def post(self):
        user = users.get_current_user().user_id()
        event_name = self.request.get('event_name')
        #TransmittedDataa = OrganizerData(user = user, eventName=eventName)
        #TransmittedData.put()

    def get(self):
        content = JINJA_ENV.get_template("templates/divsForCalendar.html")
        eventInfo = Event.query().get()
        logout = users.create_logout_url('/')

        self.response.write(content.render(logout=logout, eventInfo=eventInfo))

        #self.redirect('/volunteer')


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/volunteer', VolunteerHandler),
    ('/organizer', OrganizerHandler)
], debug=True)
