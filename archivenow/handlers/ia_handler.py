import requests

class IA_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Internet Archive'
        self.api_required = False

    def push(self, uri_org, p_args=[]):
        msg = ''
        try:
            uri = 'https://web.archive.org/save/' + uri_org
            archiveTodayUserAgent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
            # push into the archive
            r = requests.get(uri, timeout=120, allow_redirects=True, headers=archiveTodayUserAgent)
            r.raise_for_status()
            # extract the link to the archived copy 
            if (r != None):
                if "Location" in r.headers:
                    return r.headers["Location"]
                elif "Content-Location" in r.headers:
                    if (r.headers["Content-Location"]).startswith("/web/"):
                        return "https://web.archive.org"+r.headers["Content-Location"]
                    else:
                        try:
                            uri_from_content = "https://web.archive.org" + r.text.split('var redirUrl = "',1)[1].split('"',1)[0]
                        except:
                            uri_from_content = r.headers["Content-Location"]
                            #pass;
                        return uri_from_content
                else:
                    for r2 in r.history:
                        if 'Location' in r2.headers:
                            return r.url
                            #return r2.headers['Location']
                        if 'Content-Location' in r2.headers:
                            return r.url
                            #return r2.headers['Content-Location']
            msg = "("+self.name+ "): No HTTP Location/Content-Location header is returned in the response"               
        except Exception as e:
            if msg == '':
                msg = "Error (" + self.name+ "): " + str(e)
            pass;      
        return msg
