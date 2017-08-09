import requests
import json

class CC_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Perma.cc Archive'
        self.api_required = True

    def push(self, uri_org, p_args):
        msg = ''
        try:

            APIKEY = p_args['cc_api_key']

            r = requests.post('https://api.perma.cc/v1/archives/?api_key='+APIKEY, timeout=120,
                                                           data=json.dumps({"url":uri_org}),
                                                           headers={'Content-type': 'application/json'},
                                                           allow_redirects=True)       
            r.raise_for_status()

            if 'Location' in r.headers:
                return 'https://perma.cc/'+r.headers['Location'].rsplit('/',1)[1]
            else:
                for r2 in r.history:
                    if 'Location' in r2.headers:
                        return 'https://perma.cc/'+r2.headers['Location'].rsplit('/',1)[1]
            entity_json = r.json()
            if 'guid' in entity_json:
                return str('https://perma.cc/'+entity_json['guid'])
            msg = "Error ("+self.name+ "): No HTTP Location header is returned in the response" 
        except Exception as e:
            if (msg == '') and ('_api_key' in str(e)):
                msg = "Error (" + self.name+ "): " + 'An API KEY is required '
            elif (msg == ''):
                msg = "Error (" + self.name+ "): " + str(e)
            pass;
        return msg
