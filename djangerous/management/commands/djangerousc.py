from django.core.management.base import NoArgsCommand
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from djangerous.models import Post
import urllib
import re
from datetime import tzinfo, timedelta, datetime

TIMEZON_REGEXP = u''
DATE_REGEXP = re.compile(r"""
    # Sat, 31 Jul 2010 02:14:26 -0700
    ^[A-Za-z]{3},\s
    (?P<datetime>\d{2}\s[A-Za-z]{3}\s\d{4}\s\d{2}:\d{2}:\d{2}) 
    \s
    (?P<tzsign>-?)
    (?P<tzhours>\d{2})
    (?P<tzminutes>\d{2})$
    """, re.VERBOSE)
    
class Timezone(tzinfo):
    """
    Concrete implementation of abstract tzinfo. May be instantiated with a 
    match for DATE_REGEXP. If instantiated with nothing represents no shift, 
    which is UTC
    """
    def __init__(self, datem=None):
        if datem:
            self.hours = int('%s%s' % 
                (datem.group('tzsign'), datem.group('tzhours')))
            self.minutes = int('%s%s' % 
                (datem.group('tzsign'), datem.group('tzminutes')))
    def utcoffset(self, dt):
        if hasattr(self, 'hours'):
            return timedelta(hours=self.hours, minutes=self.minutes)
        else: 
            return timedelta(hours=0)
    def dst(self, dt):
        return timedelta(0)
        
UTC = Timezone()


def expandEntities(st):
    st = re.sub(u'&lt;', '<', st)
    st = re.sub(u'&gt;', '>', st)
    st = re.sub(u'&quot;', '"', st)
    st = re.sub(u'&apos;', "'", st)
    st = re.sub(u'&lt;', '<', st)
    st = re.sub(u'&amp;', '&', st)
    return st
    
def tidybody(st):
    st = expandEntities(st)
    st = re.sub(u'^\s*|\s*$', '', st)
    return st

"""
Todo
====

- Account to settings

Unit tests
----------
- Changes in XML schema
- Date format change on new posts and old
- Unable to connect/timeout
"""

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        xmlurl = 'http://posterous.com/api/readposts?hostname=benglynn'
        response = urllib.urlopen(xmlurl)
        tree = ElementTree()
        tree.parse(response)
        for postel in tree.findall('post'):
            
            id = postel.find('id').text
            link = postel.find('link').text
            body = tidybody(postel.find('body').text)
            xml = tostring(postel)
            title = postel.find('title').text
            date = None
            datest = postel.find('date').text
            datem = re.match(DATE_REGEXP, datest)
            if datem:
                # If the date in the response correct format, create datetime
                date = datetime.strptime(datem.group(1), 
                    '%d %b %Y %H:%M:%S')
                # Add timezone ('z' not supported in strptime)
                date = date.replace(tzinfo=Timezone(datem))
                # Convert to UTC
                date = date.astimezone(UTC)
            
            try:
                post = Post.objects.get(id=id)
                print 'Updating post %s' % id
            except Post.DoesNotExist:
                print 'Creating post %s' % id
                post = Post()
                post.id = id
                post.date = datetime.now()
                
            post.title = title
            if date: 
                post.date = date
            post.body = body
            post.xml = xml
            post.save()
                
                
                
# Example post xml
"""
<post>
  <url>http://post.ly/pZZZ</url>
  <link>http://benglynn.posterous.com/thats-strange</link>
  <title>That's strange</title>
  <id>24637749</id>
  <body>
    &lt;img src="http://posterous.com/getfile/files.posterous.com/benglynn/5DLot9Ecnty6JEAFZBDgyJYbo6fVJosRf0pfXHFI3Ixoi5sA6pmA2jFKH2zk/Graham_eats_his_foot_by_bengly.jpeg" width="500" height="375"/&gt;
&lt;p&gt;Very odd, the API exposes the body of the post in a CDATA section.&lt;/p&gt;&lt;p /&gt;&lt;div&gt;All paragraphs except the fist are wrapped in a DIV and preceded by a P.&lt;/div&gt;&lt;p /&gt;&lt;div&gt;&lt;i&gt;Formatting&lt;/i&gt; like &lt;b&gt;bold&lt;/b&gt; and so on is preserved. Trying some &lt;span style="background-color: rgb(255, 255, 102);"&gt;more elaborate&lt;/span&gt; stuff:&lt;/div&gt; &lt;div&gt;&lt;ol&gt;&lt;li&gt;In this&lt;/li&gt;&lt;li&gt;Post&lt;/li&gt;&lt;/ol&gt;&lt;div style="text-align: right;"&gt;And this paragraph, aligned right.&lt;/div&gt;&lt;/div&gt;&lt;p /&gt;&lt;div&gt;And what about media? Attaching an image to this post.&lt;/div&gt;
  </body>
  <date>Sat, 31 Jul 2010 02:14:26 -0700</date>
  <views>7</views>
  <private>false</private>
  <author>Ben Glynn</author>
  <authorpic>http://posterous.com/images/profile/unknown35.gif</authorpic>
  <commentsenabled>true</commentsenabled>
  <media>
    <type>image</type>
    <medium>
      <url>http://posterous.com/getfile/files.posterous.com/benglynn/5DLot9Ecnty6JEAFZBDgyJYbo6fVJosRf0pfXHFI3Ixoi5sA6pmA2jFKH2zk/Graham_eats_his_foot_by_bengly.jpeg</url>
      <filesize>94</filesize>
      <height>375</height>
      <width>500</width>
    </medium>
    <thumb>
      <url>http://posterous.com/getfile/files.posterous.com/benglynn/i41C8Ygpth6XksK1ydolH9SYM2WafJt8em8DCT8X7x3jUDSUR3XlvZIzbdLd/Graham_eats_his_foot_by_bengly.jpeg.thumb.jpg</url>
      <filesize>94</filesize>
      <height>36</height>
      <width>36</width>
    </thumb>
  </media>
  <commentsCount>0</commentsCount>
</post>
"""