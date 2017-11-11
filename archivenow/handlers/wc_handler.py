import random
import string
import requests


class WC_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The WebCite Archive'
        self.api_required = False 

    # generate an email required to push pages
    def generate_random_email(self):
        ''' From http://codereview.stackexchange.com/questions/
            58269/generating-random-email-addresses '''
        nb = 1
        length = 7
        domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
        letters = string.ascii_lowercase[:12]
        def get_random_domain(domains):
            return random.choice(domains)
        def get_random_name(letters, length):
            return ''.join(random.choice(letters) for i in range(length))
        return [get_random_name(letters, length) + '@' + get_random_domain(domains) for i in range(nb)][0]

    def page_exists_in_wc(self,urim):
        try:
            r = requests.get(urim, timeout=180, 
                            allow_redirects=True)                  

            r2 = requests.get('http://www.webcitation.org/mainframe.php', timeout=180, cookies=r.cookies,
                            allow_redirects=True)  

            if ("When WebCite tried to archive the page, it received a Page Not Found error" in r2.text):   
                return False
            else:
                return True    
        except:
            pass;
        return False        


    def push(self, uri_org):
        msg = ''
        try:
            # push to the archive
            r = requests.post('http://www.webcitation.org/archive', timeout=180, 
                                                                    data={'url':uri_org, 'email':self.generate_random_email()}, 
                                                                    allow_redirects=True)
            r.raise_for_status()
            # extract the link to the archived copy
            if (r != None):
                out = r.text
                try: 
                    urim = 'http://www.webcitation.org/' + out.split('http://www.webcitation.org/')[1][0:9] 
                except:
                   msg = "IndexError (" + self.name+ "): unable to extract a URL to the archived version from the response "
                   raise  
            # check if the page is archived 
            if not self.page_exists_in_wc(urim):
                msg = "Error (" + self.name+ "): " + " Received a Page Not Found error from the website concerned"
            else:
                return str(urim)                                            
        except Exception as e:
            if msg == '':
                msg = "Error (" + self.name+ "): " + str(e)
            pass;
        return str(msg)
