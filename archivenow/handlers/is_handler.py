import requests

class IS_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Archive Today'

    def push(self, uri_org):
        try:

            archiveTodaySubmitId = ""
            archiveTodayUserAgent = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" }

            # get the newest submitid required to push pages
            rid = requests.get('http://archive.is/', timeout=120, allow_redirects=True, headers=archiveTodayUserAgent)
            htmldata = str(rid.content)
            archiveTodaySubmitId = htmldata.split('name="submitid',1)[1].split('value="',1)[1].split('"',1)[0]

            # push to the archive
            r = requests.post('http://archive.is/submit/', timeout=120,
                                                           data={"anyway":"1" , "url":uri_org, "submitid":archiveTodaySubmitId},
                                                           allow_redirects=True,
                                                           headers=archiveTodayUserAgent)
            # extract the link to the archived copy
            if 'Refresh' in r.headers:
                return str(r.headers['Refresh']).split(';url=')[1]
            else:
                if 'Location' in r.headers:
                    return r.headers['Location']
                else:
                    for r2 in r.history:
                        if 'Location' in r2.headers:
                            return r2.headers['Location']
        except Exception as e:
            pass;
        return self.name+ ": Unexpected error"
