import requests

class IS_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Archive.is'
        self.api_required = False 

    def push(self, uri_org):
        msg = ''
        try:

            archiveTodaySubmitId = ""
            archiveTodayUserAgent = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" }

            # get the newest submitid required to push pages
            rid = requests.get('http://archive.is/', timeout=120, allow_redirects=True, headers=archiveTodayUserAgent)
            rid.raise_for_status()
            htmldata = str(rid.content)
            
            try:
                archiveTodaySubmitId = htmldata.split('name="submitid',1)[1].split('value="',1)[1].split('"',1)[0]
            except: 
                msg = "IndexError (" + self.name+ "): unable to extract 'submitid' "
                raise  

            # push to the archive
            r = requests.post('http://archive.is/submit/', timeout=120,
                                                           data={"anyway":"1" , "url":uri_org, "submitid":archiveTodaySubmitId},
                                                           allow_redirects=True,
                                                           headers=archiveTodayUserAgent)          
            r.raise_for_status()
            # extract the link to the archived copy
            if 'Refresh' in r.headers:
                try:
                    return str(r.headers['Refresh']).split(';url=')[1]
                except:
                   msg = "IndexError (" + self.name+ "): unable to extract a URL to the archived version from HTTP Refresh header ("+str(r.headers['Refresh'])+")"
                   raise 
            else:
                if 'Location' in r.headers:
                    return r.headers['Location']
                else:
                    for r2 in r.history:
                        if 'Location' in r2.headers:
                            return r2.headers['Location']
            msg = "Error ("+self.name+ "): No HTTP Location/Refresh header is returned in the response" 
        except Exception as e:
            if msg == '':
                msg = "Error (" + self.name+ "): " + str(e)
            pass;
        return msg
