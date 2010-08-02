from django.core.management.base import NoArgsCommand
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from djangerous.models import Post
import urllib
import re
from datetime import datetime

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        xmlurl = 'http://posterous.com/api/readposts?hostname=benglynn'
        response = urllib.urlopen(xmlurl)
        tree = ElementTree()
        tree.parse(response)
        for post in tree.findall('post'):
            
            id = post.find('id').text
            title = post.find('title').text
            date = post.find('date').text
            
            try:
                post = Post.objects.get(id=id)
                print 'Updating post %s' % id
            except Post.DoesNotExist:
                print 'Creating post %s' % id
                post.id = id
            print 
            print title
            # Sat, 31 Jul 2010 02:14:26 -0700
            #http://docs.python.org/library/datetime.html
            # Strip superfluous day and UTC offset from date (not supported in
            # strptime) todo - check format aginst regex before parsing?
            strip = re.sub(u'^[A-Za-z]{3},\s(.*)\s-?\d{4}$', '\g<1>', date)
            dt = datetime.strptime(strip, '%d %b %Y %H:%M:%S')
            print dt
            # todo - feed in UTC offset
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