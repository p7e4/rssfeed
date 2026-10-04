from email.utils import parsedate_to_datetime
from xml.etree import ElementTree
from datetime import datetime

__version__ = "0.5.0"

class ParseError(Exception):
    pass

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

def parse(data):
    if not (data:=data.lstrip()): raise ParseError("empty data")
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        raise ParseError("xml parse fail") from e

    if not root.tag.endswith(("feed", "rss", "RDF")):
        raise ParseError("not rss")

    for e in root.iter():
        if e.tag[0] == "{":
            e.tag = e.tag.rpartition("}")[2]

    if root.tag == "rss": root = root.find("channel")
    if root is None: raise ParseError("no channel elem found")
    baseUrl = e.text or e.get("href") if (e:=root.find("link")) is not None else None
    if baseUrl and (i:=baseUrl.find("/", 8)) > 0:
        baseUrl = baseUrl[:i]

    def findText(*x):
        for i in x:
            if (a:=e.findtext(i)) and (a:=a.strip()):
                return a
        return str()

    def findLink(e):
        link = e.find("link")
        if link is not None:
            if link.get("rel") in ("related", "replies"):
                link = e.find("link[@rel='alternate']")
            link = link.text.strip() if link.text else link.get("href")

        if not link and (a:=findText("guid", "id")).startswith("http"):
            link = a

        if baseUrl and link and not link.startswith(("http://", "https://")):
            return f"{baseUrl}/{link.lstrip("/")}"
        return link or str()

    items = list()
    for e in root.iterfind("entry" if root.tag == "feed" else "item"):
        items.append({
            "title": findText("title"),
            "author": findText("author", "author/name", "creator"),
            "timestamp": timeParse(findText("pubDate", "published", "updated", "date")),
            "url": findLink(e),
            "content": findText("content", "encoded", "description", "summary")
        })
    return {
        "name": root.findtext("title") or root.findtext("channel/title") or str(),
        "lastupdate": max(i["timestamp"] for i in items) if items else 0,
        "items": items,
    }

def opmlParse(data):
    if not (data:=data.lstrip()): raise ParseError("empty data")
    parser = ElementTree.XMLPullParser(("start", "end"))
    try:
        parser.feed(data)
        parser.close()
    except Exception as e:
        raise ParseError("xml parse fail") from e

    path = list()
    result = dict(default=list())
    for event, elem in parser.read_events():
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

    if not result.get("default"):
        del result["default"]

    return result
