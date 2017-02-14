import random
import string
import requests


class WC_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The WebCite Archive'

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

    def push(self, uri_org):
        try:
            # push to the archive
            r = requests.post('http://www.webcitation.org/archive', timeout=180, 
                                                                    data={'url':uri_org, 'email':self.generate_random_email()}, 
                                                                    allow_redirects=True)
            # extract the link to the archived copy
            if (r != None):
                out = r.text 
                return 'http://www.webcitation.org/' + out.split('http://www.webcitation.org/')[1][0:9]            
        except Exception as e:
            pass;
        return self.name+ ": Unexpected error"
