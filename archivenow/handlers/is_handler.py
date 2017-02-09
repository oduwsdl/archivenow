import os
import sys
import subprocess
from bs4 import BeautifulSoup
import logging

PATH = str(os.path.dirname(os.path.abspath(__file__)))

# to import util.py
sys.path.append(PATH + '/..')
from util import *


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=PATH + '/../debug.log',
                    filemode='a')

class IS_handler(object):

	def __init__(self):
		self.enabled = True
		self.name = 'The Archive Today'
		self.urim = None

	def push(self, uri_org):	
		try:
			self.urim = None
			archiveTodaySubmitId = ""
			archiveTodayUserAgent = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" }	

			# get the newest submitid
			cmd = (" curl -i http://archive.is/ ");
			p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = p.communicate()
			if len(out.rstrip())>10:
				soup = BeautifulSoup(out, "html.parser")
				archiveTodaySubmitId = soup.input['value']

			r = sendPostRequest('http://archive.is/submit/',{"anyway":"1" , "url":uri_org, "submitid":archiveTodaySubmitId}, archiveTodayUserAgent)

			if 'Refresh' in r.headers:
				self.urim = str(r.headers['Refresh']).split(';url=')[1]
				return self.urim		
			else:
				if 'Location' in r.headers:
					self.urim = r.headers['Location']
					return self.urim
				else: 
					for r2 in r.history:
						if 'Location' in r2.headers:
							self.urim = r2.headers['Location']
							return self.urim
		except Exception as e:
			logging.error(e)
			return None



