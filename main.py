import os
import json
import webapp2
import jinja2
import helpers

from datetime import datetime

from itertools import imap

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

        # THIS WILL BREAK AT THE END OF DEC OR EARLY JAN.

        #year = Event.start_time.year
        week = helpers.get_this_week()
        start_week = datetime(2018, week[0][0], week[0][1], 0, 0)
        end_week = datetime(2018, week[-1][0], week[-1][1], 0, 0)

        events = Event.query().filter(ndb.AND(
                Event.start_time >= start_week,
                Event.start_time <= end_week
        )).fetch()

        logout = users.create_logout_url('/')
        
        listOfDays=["Sun","Mon","Tues","Wed","Thurs","Fri","Sat"]
        
        for i in range(len(week)):
            week[i].append(listOfDays[i]);

        def _get_dow(t):
            return listOfDays[helpers._dow(t.month, t.day, t.year)]

        def _get_time(t):
            return t.hour

        data = []
        for event in events:
            start_dow = _get_dow(event.start_time)
            end_dow = _get_dow(event.final_time)

            start_time = event.start_time.hour
            end_time = event.final_time.hour

            data.append([
                    " ".join([start_dow, str(start_time)]),
                    " ".join([end_dow, str(end_time)]),
                    event.event_name
            ])

        print(data)

        self.response.write(content.render(
            week = imap(lambda x: x[2] + " " + str(x[0]) + "/" + str(x[1])
                , week), data = json.dumps(data), logout=logout))

        #self.redirect('/volunteer')


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/volunteer', VolunteerHandler),
    ('/organizer', OrganizerHandler)
], debug=True)
