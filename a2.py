# -*- coding:utf-8 -*-  

import tornado.ioloop  
import tornado.web  
import tornado.options
import tornado.autoreload
import tornado.httpserver
settings = {'debug' : True}
#define("debug",default=True,help="Debug Mode",type=bool)
 
class MyFormHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('<html><body><form action="/" method="POST">'
				   '<input type="text" name="message">'
				   '<input type="submit" value="Submit">'
				   '</form></body></html>')

	def post(self):
		self.set_header("Content-Type", "text/plain")
		self.write("You wrote " + self.get_body_argument("message"))
		self.write("You wrote ") 
		
		
application = tornado.web.Application([  
	(r"/",MyFormHandler),  
	
],**settings)  
  
if __name__=="__main__":  
	application.listen(28888)  
	tornado.ioloop.IOLoop.instance().start()  
