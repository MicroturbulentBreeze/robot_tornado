# -*- coding:utf-8 -*-  

import tornado.ioloop  
import tornado.web  
import tornado.options
import tornado.autoreload
import tornado.httpserver
from tornado.options import define, options
import aiml
import os
#from config import *
settings = {'debug' : True}
define("debug",default=True,help="Debug Mode",type=bool)
alice=""

def alice_init():
	os.chdir('/home/wangxin/alice')
	alice = aiml.Kernel()
	alice.learn("startup.xml")
	alice.respond('LOAD ALICE')
	return alice
class MainHandler(tornado.web.RequestHandler):  
	def get(self):  
		self.write('<html><body><form action="/" method="post">'
				   '<input type="text" name="message">'
				   '<input type="submit" value="Submit">'
				   '</form></body></html>') 
	def post(self):
		#self.set_header("Content-Type", "text/plain")
		#print "aaa"
		#print self.get_argument("message")
		self.write("You wrote " + self.get_argument("message")) 
		self.write("You wrote " + self.get_argument("message")) 

class AliceHandler(tornado.web.RequestHandler):

	def get(self):
		req = self.get_argument('req', 'default')
		#self.write("haha")
		if req and req != 'default':
			#self.write(req)
			self.write(alice.respond(req))

	def post(self):
		self.write('this is the POST method !')		  
  
if __name__=="__main__":  
	alice=alice_init()
	application = tornado.web.Application([  
		(r"/",MainHandler),  
		(r"/alice",AliceHandler), 
	],**settings)
		
	application.listen(28888)  
	tornado.ioloop.IOLoop.instance().start()  
	
