import os
import requests

new_header = 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'


class MG_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'Megalodon.jp'
        self.api_required = False

    def push(self, uri_org, p_args=[]):

        if not uri_org.startswith('http'):
            uri_org = 'http://' + uri_org

        msg = ''
        try:

            headers = {
                'User-Agent': new_header,
            }

            try:
                r = requests.get('http://megalodon.jp/?url=' + uri_org,
                                 headers=headers)
                token = str(r.content).split('"token" value="',
                                             1)[1].split('"',1)[0]

                phpsessid = r.headers['Set-Cookie'].split('PHPSESSID=', 1)[1]
                phpsessid = phpsessid.split(';', 1)[0]

                cookies = dict(PHPSESSID=phpsessid)

            except Exception as e:
                msg = "Error ({0}): {1}".format(self.name, str(e))

            try:
                r2 = requests.post('http://megalodon.jp/pc/get_simple/decide',
                                data={"url":uri_org, "token":token},
                                cookies=cookies, headers=headers,
                                )
            except Exception as e:
                msg = "Error ({0}): {1}".format(self.name, str(e))

            msg = str(r2.content).split('location.href = "',
                                        1)[1].split('"', 1)[0]
        except Exception as e:
            if not msg:
                msg = "Error (" + self.name+ "): " + str(e)
            pass;
        if ('list index out of range' in msg) or ('referenced before assignment' in msg):
            msg = "Error (" + self.name+ "): " + "We can not obtain this page because the time limit has been reached or for technical ... "
        return msg
