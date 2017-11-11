import requests

class IA_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Internet Archive'
        self.api_required = False

    def push(self, uri_org):
        msg = ''
        try:
            uri = 'https://web.archive.org/save/' + uri_org
            # push into the archive
            r = requests.get(uri, timeout=120, allow_redirects=True)
            r.raise_for_status()
            # extract the link to the archived copy 
            if (r != None):
                if "Location" in r.headers:
                    return r.headers["Location"]
                elif "Content-Location" in r.headers:
                    return "https://web.archive.org"+r.headers["Content-Location"]    
                else:
                    for r2 in r.history:
                        if 'Location' in r2.headers:
                            return r2.headers['Location']
                        if 'Content-Location' in r2.headers:
                            return r2.headers['Content-Location']
            msg = "("+self.name+ "): No HTTP Location/Content-Location header is returned in the response"               
        except Exception as e:
            if msg == '':
                msg = "Error (" + self.name+ "): " + str(e)
            pass;      
        return msg
