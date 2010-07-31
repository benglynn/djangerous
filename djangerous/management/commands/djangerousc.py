from django.core.management.base import NoArgsCommand
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from djangerous.models import Post
import urllib2

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        # create a password manager, build opener and install
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        top_level_url = 'http://posterous.com/api/readposts'
        password_mgr.add_password(None, top_level_url, 'benglynn@benglynn.net', 'melody2229')
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        req = urllib2.Request(top_level_url)
        response = urllib2.urlopen(req)
        print response.read()