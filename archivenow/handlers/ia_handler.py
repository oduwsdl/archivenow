import requests

class IA_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Internet Archive'

    def push(self, uri_org):
        try:
            uri = 'https://web.archive.org/save/' + uri_org
            # push into the archive
            r = requests.get(uri, timeout=120, allow_redirects=True)
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
        except Exception as e:
            pass;  
        return self.name+ ": Unexpected error"
