from django.core.management.base import NoArgsCommand
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from djangerous.models import Post
import urllib

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        xmlurl = 'http://posterous.com/api/readposts?hostname=benglynn'
        response = urllib.urlopen(xmlurl)
        print response.read()