import os
import sys
import random
import string
#import logging

PATH = str(os.path.dirname(os.path.abspath(__file__)))

# to import util.py
sys.path.append(PATH + '/..')
from util import *


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s %(message)s',
#                     filename='/tmp/archivenow_debug.log',
#                     filemode='a')

class WC_handler(object):

	def __init__(self):
		self.enabled = True
		self.name = 'The WebCite Archive'
		self.urim = None

	# save a web page in webcitation.org
	def generate_random_email(self):
		''' From http://codereview.stackexchange.com/questions/
			58269/generating-random-email-addresses '''
		nb = 1
		length = 7
		domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
		letters = string.ascii_lowercase[:12]
		def get_random_domain(domains):
		    return random.choice(domains)
		def get_random_name(letters, length):
		    return ''.join(random.choice(letters) for i in range(length))
		return [get_random_name(letters, length) + '@' + get_random_domain(domains) for i in range(nb)][0]

	def push(self, uri_org):	
		try:
			r = sendPostRequest('http://www.webcitation.org/archive',{'url':uri_org, 'email':self.generate_random_email()})
			if (r != None):
				out = r.content 
				self.urim = 'http://www.webcitation.org/' + out.split('http://www.webcitation.org/')[1][0:9]
				return self.urim		
		except:
		    # Exception as e:
			#logging.error(e)
			#print (e)
			pass;
		return None









