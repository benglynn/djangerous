from django.core.management.base import NoArgsCommand
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from djangerous.models import Post

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        """
        Poll posterous for photos and update database
        """
        print 'todo'
        