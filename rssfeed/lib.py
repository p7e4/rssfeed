from dateutil.parser import parse as timeParse
from xml.etree import ElementTree

__version__ = "0.4.1"

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

def parse(data):
    items = list()
    for event, elem in _parse(data).read_events():
        tag = elem.tag.split("}", 1)[1] if elem.tag.startswith("{") else elem.tag
        text = elem.text.strip() if elem.text else str()
        if event == "start":
            if tag in ("channel", "RDF", "feed", "item", "entry"):
                items.append({
                    "title": str(),
                    "author": str(),
                    "timestamp": 0,
                    "url": str(),
                    "content": str()
                })
        else:
            i = items[-1]
            match tag:
                case "description" | "encoded" | "summary" | "content":
                    i["content"] = text
                case "pubDate" | "updated" | "published" | "lastBuildDate":
                    if text.isdigit():
                        i["timestamp"] = int(text)
                    elif text:
                        try:
                            i["timestamp"] = int(timeParse(text).timestamp())
                        except Exception as e:
                            raise ParseError("time parse fail") from e
                    # if len(items) and items[0]["timestamp"] < i["timestamp"]:
                    #     items[0]["timestamp"] = i["timestamp"]
                case "link":
                    i["url"] = text or elem.get("href")
                case "title" | "author":
                    i[tag] = text


    if not items:
        raise ParseError("not valid result")

    feed = {
        "name": items[0]["title"],
        "lastupdate": items[0]["timestamp"],
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
