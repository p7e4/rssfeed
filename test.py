import rssfeed
opml = """
<?xml version="1.0" encoding="UTF-8"?>
<opml version='1.1'>
  <head>
    <title>Frontend Dev Feeds</title>
  </head>
  <body>
    <outline text="frontend-webapps">
      <outline htmlUrl="http://aerotwist.com/blog/feed/" xmlUrl="http://aerotwist.com/blog/feed/" type="rss" description="" text="Aerotwist Blog"/>
      <outline htmlUrl="http://alexsexton.com" xmlUrl="http://alexsexton.com/?feed=rss2" type="rss" description="" text="Alex Sexton"/>
      <outline text="frontend">
        <outline htmlUrl="https://addyosmani.com/" xmlUrl="https://addyosmani.com/rss.xml" type="rss" description="" text="AddyOsmani.com"/>
        <outline htmlUrl="http://blog.nodejitsu.com/" xmlUrl="http://blog.nodejitsu.com/feed.xml" type="rss" description="" text="blog.nodejitsu.com"/>
      </outline>
    </outline>
    <outline htmlUrl="http://blogs.opera.com/mobile" xmlUrl="http://blogs.opera.com/mobile/feed/" type="rss" description="" text="Opera Mobile"/>
    <outline htmlUrl="http://blogs.windows.com/msedgedev" xmlUrl="http://blogs.msdn.com/b/ie/atom.aspx" type="rss" description="" text="IEBlog"/>
  </body>
</opml>
"""
import json
print(json.dumps(rssfeed.opmlParse(opml), indent=4))