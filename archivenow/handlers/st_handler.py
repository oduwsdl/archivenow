import os
import requests
import re

new_header = 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'

headers = {'User-Agent': new_header}

r_url = re.compile('<a href="(http\S+)" target=_blank>archive here</a>')
re_exists_url = re.compile("archive here: <a href=(http\S+?)>http\S+?</a></h3>")

class ST_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Archive.st'
        self.api_required = False

    def push(self, uri_org, p_args=[]):
        msg = ''

        try:
            post_data = {"url": uri_org}
            r = requests.post("https://archive.st/archive.php",
                              data=post_data, headers=headers)

            page = str(r.content)

            if page in "<div class='alert'>The Captcha is invalid. Please try again.</div>":
                raise ValueError('The Captcha is invalid.')

            results = r_url.findall(page)

            if results:
                msg = results[0]
            elif "ERROR" in page:
                new_results = re_exists_url.findall(page)
                msg = new_results[0]
            msg = msg.replace('http://', 'https://')
            msg = msg.replace('Archive.st', 'archive.st')

        except Exception as e:
            msg = "ERROR ({0}): {1}".format(self.name,e)

        return msg
