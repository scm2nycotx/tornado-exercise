import tornado.ioloop
import tornado.web
import tornado.log

import os
import boto3

client = boto3.client(
  'ses',
  region_name="us-east-1",
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
)

from jinja2 import \
  Environment, PackageLoader, select_autoescape

ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    name = self.get_query_argument("name", "Nobody")
    amount = self.get_query_argument("amount", "0")
    amount = float(amount)
    amount = amount * 1.15
    context = {
      "name" : name,
      "users" : ["Sam", "mittens", "Chih-Ming"],
      "amount" : amount
    }
    self.render_template("hello.html", context)
    

class PageHandler(TemplateHandler):
  def get(self, page):
    page = page + ".html"
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template(page, {})
    
def send_email (email, comments):
  response = client.send_email(
    Destination={
      'ToAddresses': ['scm2nycotx@gmail.com'],
    },
    Message={
      'Body': {
        'Text': {
          'Charset': 'UTF-8',
          'Data': '{} wants to talk to you\n\n{}'.format(email, comments),
        },
      },
      'Subject': {'Charset': 'UTF-8', 'Data': 'Test email'},
    },
    Source='scm2nycotx@gmail.com',
  )
class Form1Handler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("form1.html", {})
    
class FormHandler(TemplateHandler):
  def get(self):
    search = self.get_query_argument('query', None)
    print(search)
    # do a look up in my database
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("form.html", {})
  
  def post(self):
    email = self.get_body_argument('email', None)
    comments = self.get_body_argument("comments", None)
    error = ""
    if email:
      print("EMAIL:", email)
      send_email(email, comments)
      self.redirect("/form-success")
    
    else:
      error = "GIVE ME YOUR EMAIL!"
    
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("form.html", {"error": error})

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/form1", Form1Handler),
    (r"/form", FormHandler),
    (r"/(page2)", PageHandler),
    (r"/(form-success)", PageHandler),
    (
      r"/static/(.*)", 
      tornado.web.StaticFileHandler,
      {'path': 'static'}
    ),
  ], autoreload=True)
  
if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  
  PORT = os.environ.get('PORT', 8080)
  app = make_app()
  app.listen(PORT)
  tornado.ioloop.IOLoop.current().start()