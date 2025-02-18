# rssfeed

A simple rss/atom/opml parser

## Installation

`pip install rssfeed`


## Get Started

### rss parse

``` python
import requests
import rssfeed

text = requests.get("https://lobste.rs/rss").text
rssfeed.parse(text)
```

``` json
{
    "name": "Lobsters",
    "lastupdate": 1739824193,
    "items": [
        {
            "title": "Why I'm Writing a Scheme Implementation in 2025 (The Answer is Async Rust)",
            "author": "maplant.com by mplant",
            "timestamp": 1739824193,
            "url": "https://maplant.com/2025-02-17-Why-I'm-Writing-a-Scheme-Implementation-in-2025-(The-Answer-is-Async-Rust).html",
            "content": "<p><a href=\"https://lobste.rs/s/zm1g8r/why_i_m_writing_scheme_implementation\">Comments</a></p>"
        },
        {
            "title": "14 years of systemd",
            "author": "lwn.net via calvin",
            "timestamp": 1739814564,
            "url": "https://lwn.net/SubscriberLink/1008721/7c31808d76480012/",
            "content": "<p><a href=\"https://lobste.rs/s/c6rk0l/14_years_systemd\">Comments</a></p>"
        },
        {
            "title": "Making the Web More Readable With Stylus",
            "author": "wezm.net by wezm",
            "timestamp": 1739757928,
            "url": "https://www.wezm.net/v2/posts/2025/stylus/",
            "content": "<p><a href=\"https://lobste.rs/s/sag0p3/making_web_more_readable_with_stylus\">Comments</a></p>"
        }
    ]
}
```

> rssfeed **does not** escape HTML tag, which mean if you does not check the content and display it somewhere html can be rendered, it may lead to [Cross-site scripting](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting) attacks.


### opml parse

``` python
import rssfeed
opml = """
<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
  <head>
    <title>demo feeds</title>
  </head>
  <body>
    <outline text="news">
      <outline text="奇客Solidot" xmlUrl="https://www.solidot.org/index.rss" type="rss" />
      <outline text="news-submenu">
        <outline text="Lobsters" xmlUrl="https://lobste.rs/rss" type="rss" />
      </outline>
    </outline>
    <outline text="阮一峰的网络日志" xmlUrl="https://feeds.feedburner.com/ruanyifeng" type="rss" />
  </body>
</opml>
"""
rssfeed.opmlParse(opml)
````

``` json
{
    "default": [
        {
            "name": "阮一峰的网络日志",
            "url": "https://feeds.feedburner.com/ruanyifeng"
        }
    ],
    "news": [
        {
            "name": "奇客Solidot",
            "url": "https://www.solidot.org/index.rss"
        },
        {
            "name": "Lobsters",
            "url": "https://lobste.rs/rss"
        }
    ]
}
```

as you can see, a two-layer structure will always be generated regardless of the original structure. If the original file includes multiple levels, only the outermost menu is retained. If a feed on the root it will be place in `default` menu.

