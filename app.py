import tornado.ioloop
import tornado.web
import tornado.log

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
    

class Page2Handler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("page2.html", {})

class Form1Handler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("form1.html", {})

class FormHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("form.html", {})
  
  def post(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("form.html", {})

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/form1", Form1Handler),
    (r"/form", FormHandler),
    (r"/page2", Page2Handler),
    (
      r"/static/(.*)", 
      tornado.web.StaticFileHandler,
      {'path': 'static'}
    ),
  ], autoreload=True)
  
if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  
  app = make_app()
  app.listen(8000)
  tornado.ioloop.IOLoop.current().start()