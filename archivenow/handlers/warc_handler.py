import requests
import os.path
import distutils.spawn

class WARC_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'Generate WARC file'
        self.api_required = False

    def push(self, uri_org, p_args=[]):
        msg = ''
        if p_args['agent'] == 'squidwarc':
            # squidwarc
            #if not distutils.spawn.find_executable("squidwarc"):
            #    return 'wget is not installed!'
            os.system('python ~/squidwarc_one_page/generte_warcs.py 9222 "'+uri_org+'" '+p_args['warc']+'.warc  &> /dev/null')
            if os.path.exists(p_args['warc']):
                return p_args['warc']
            elif os.path.exists(p_args['warc']+'.warc'):
                return p_args['warc']+'.warc'
            else:
                return 'squidwarc failed to generate the WARC file'

        else:
            if not distutils.spawn.find_executable("wget"):
                return 'wget is not installed!'
            # wget 
            os.system('wget -E -H -k -p -q --delete-after --no-warc-compression --warc-file="'+p_args['warc']+'" "'+uri_org+'"')
            if os.path.exists(p_args['warc']):
                return p_args['warc']
            elif os.path.exists(p_args['warc']+'.warc'):
                return p_args['warc']+'.warc'
            else:
                return 'wget failed to generate the WARC file'
