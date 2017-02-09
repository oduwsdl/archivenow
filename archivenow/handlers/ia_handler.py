import os
import sys
#import logging

PATH = str(os.path.dirname(os.path.abspath(__file__)))

# to import util.py
sys.path.append(PATH + '/..')
from util import *

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s %(message)s',
#                     filename='/tmp/archivenow_debug.log',
#                     filemode='a')

class IA_handler(object):

	def __init__(self):
		self.enabled = True
		self.name = 'The Internet Archive'
		self.urim = None

	def push(self, uri_org):	
		try:
			self.urim = None
			uri = 'https://web.archive.org/save/' + uri_org

			r = sendGetRequest(uri)
			if (r != None):
				if "Location" in r.headers:
					self.urim = r.headers["Location"]
					return self.urim
				elif "Content-Location" in r.headers:
					self.urim = "https://web.archive.org"+r.headers["Content-Location"]	
					return self.urim
				else:
					for r2 in r.history:
						if 'Location' in r2.headers:	
							self.urim = r2.headers['Location']				
							return self.urim
		except Exception as e:
			#logging.error(e)
			print (e)
			pass;
		return None
