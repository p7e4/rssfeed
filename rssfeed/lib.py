from email.utils import parsedate_to_datetime
from xml.etree import ElementTree
from datetime import datetime

__version__ = "0.4.5"

class ParseError(Exception):
    pass

def _parse(data):
    if not (data:=data.lstrip()):
        raise ParseError("empty data")
    parser = ElementTree.XMLPullParser(("start", "end"))
    try:
        parser.feed(data)
        parser.close()
    except ElementTree.ParseError as e:
        raise ParseError("xml parse fail") from e
    return parser

def timeParse(s):
    if not s: return 0
    try:
        if s.isdigit():
            return int(s)
        if len(s) > 4 and s[4] == "-":
            t = datetime.fromisoformat(s.replace("Z", "+00:00"))
        else:
            t = parsedate_to_datetime(s)
        return int(t.timestamp())
    except (TypeError, ValueError):
        return 0

def parse(data, url=None):
    if url: url = url[:8] + url[8:].split("/")[0]
    items = list()
    for event, elem in _parse(data).read_events():
        tag = elem.tag.rsplit("}", 1)[-1]
        if event == "start":
            if tag in ("channel", "feed", "item", "entry"):
                items.append({
                    "title": str(),
                    "author": str(),
                    "timestamp": 0,
                    "url": str(),
                    "content": str()
                })
        else:
            if not (elem.text and (text:=elem.text.strip())) and tag != "link":
                continue
            i = items[-1]
            match tag:
                case "content" | "encoded":
                    i["content"] = text
                case "summary" | "description":
                    if not i["content"]: i["content"] = text
                case "pubDate" | "published" | "date":
                    try:
                        if not i["timestamp"]: i["timestamp"] = timeParse(text)
                    except Exception as e:
                        raise ParseError("time parse fail") from e
                case "link":
                    if not i["url"]: i["url"] = elem.get("href") or text
                    if not i["url"].startswith(("http://", "https://")) and url:
                        i["url"] = f"{url}/{i["url"].lstrip("/")}"
                case "author" | "name" | "creator":
                    if not i["author"]:
                        i["author"] = text
                case "title":
                    if not i["title"]:
                        i["title"] = text

    if not items:
        raise ParseError("not valid result")

    feed = {
        "name": items[0]["title"],
        "lastupdate": max(i["timestamp"] for i in items[1:]),
        "items": items[1:]
    }

    return feed

def opmlParse(data):
    path = list()
    result = dict(default=list())
    for event, elem in _parse(data).read_events():
        if elem.tag != "outline":
            continue
        if event == "start":
            if elem.get("type") == "rss":
                name = path[0] if path else "default"
                result[name].append({
                    "name": elem.get("text") or elem.get("title"),
                    "url": elem.get("xmlUrl") or elem.get("htmlUrl")
                })
            else:
                path.append(elem.get("text") or elem.get("title"))
                if len(path) == 1: result[path[0]] = list()
        else:
            if elem.get("type") != "rss":
                path.pop()

    if not result["default"]:
        del result["default"]

    return result
