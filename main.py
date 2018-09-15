import os
import webapp2
import jinja2


JINJA_ENV = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape =True
)


class HomePage(webapp2.RequestHandler):

    def get(self):
        homepage_template = JINJA_ENV.get_template('templates/homepage.html')
        self.response.write(homepage_template.render(content="hello, world"))


class CalenderPage(webapp2.RequestHandler):

    def get(self):
        calendar_template = JINJA_ENV.get_template("templates/divsForCalendar.html")
        self.response.write(calendar_template.render())


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/calendar',CalenderPage)
], debug=True)
