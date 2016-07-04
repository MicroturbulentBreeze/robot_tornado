# -*- coding:utf-8 -*-  

import tornado.ioloop  
import tornado.web  
import tornado.options
import tornado.autoreload
import tornado.httpserver
from tornado.options import define, options
import aiml
import os
import hashlib
import xmltodict
import json;
import sys
reload(sys)
sys.setdefaultencoding('utf8') 
#from config import *
settings = {'debug' : True, 'wx_token' : 'husky', 'Token' : 'husky','wx_test':True}
define("debug",default=True,help="Debug Mode",type=bool)
alice=""

def check_wx_request(signature, timestamp, nonce):
    token = settings['wx_token']
    arr = [token, timestamp, nonce]
    arr.sort()
    sh = hashlib.sha1(arr[0] + arr[1] + arr[2]).hexdigest()
    if sh == signature:
        return True
    else:
        return False
def my_req(msg_body):
	js_msg = xmltodict.parse(msg_body)
	jsonStr = json.dumps(js_msg);
	msg = js_msg['xml']
	MsgType = msg['MsgType']

	main_content = {}
	main_content['MsgType'] = msg['MsgType']
	main_content['CreateTime'] = msg['CreateTime']
	main_content['ToUserName'] = msg['FromUserName']
	main_content['FromUserName'] = msg['ToUserName']

	main_content['MsgType'] = 'text'
	main_content['Content'] = '''Sorry I can't understand you'''
	if MsgType == 'text':
		req = msg['Content']
		respond = alice.respond(req)
		if respond == None or len(respond) < 1:
			respond = '''Sorry I can't understand you'''
		main_content['Content'] = respond
	elif MsgType == 'image':
		pass
	elif MsgType == 'voice':
		pass
	elif MsgType == 'video':
		pass
	elif MsgType == 'shortvideo':
		pass
	elif MsgType == 'location':
		pass
	elif MsgType == 'link':
		pass
	else:
		pass		
	result = {}
	result['xml'] = main_content
	return xmltodict.unparse(result)

def alice_init():
	os.chdir('/root/robot_tornado/alice')
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
		

class WeChat(tornado.web.RequestHandler):

	def get(self):
		signature = self.get_argument('signature', 'default')
		timestamp = self.get_argument('timestamp', 'default')
		nonce = self.get_argument('nonce', 'default')
		echostr = self.get_argument('echostr', 'default')
		if check_wx_request(signature, timestamp, nonce):
			self.write(echostr)
		else:
			self.write('fail')

	def post(self):
		signature = self.get_argument('signature', 'default')
		timestamp = self.get_argument('timestamp', 'default')
		nonce = self.get_argument('nonce', 'default')
		if settings['wx_test'] or (signature != 'default' and timestamp != 'default' and nonce != 'default' and check_wx_request(signature, timestamp, nonce)):
			body = self.request.body
			try:
				#self.write("success")
				self.write(my_req(body))
			except IOError, e:
				return
		
if __name__=="__main__":  
	alice=alice_init()
	application = tornado.web.Application([  
		(r"/",MainHandler),  
		(r"/alice",AliceHandler), 
		(r"/wx",WeChat), 
	],**settings)
		
	application.listen(80)  
	tornado.ioloop.IOLoop.instance().start()  
	
