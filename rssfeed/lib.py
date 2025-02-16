from dateutil.parser import parse as timeParse
from xml.etree import ElementTree

__version__ = "0.4.0"

class ParseError(Exception):
    pass

def parse(data):
    parser = ElementTree.XMLPullParser(("start", "end"))
    try:
        parser.feed(data)
        parser.close()
    except ElementTree.ParseError as e:
        raise ParseError("xml parse fail") from e

    items = list()
    lastTag = str()
    for event, elem in parser.read_events():
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
                case "content" | "description" | "encoded" | "summary":
                    i["content"] = text
                case "updated" | "pubDate" | "published" | "lastBuildDate":
                    if text.isdigit():
                        i["timestamp"] = int(text)
                    elif text:
                        try:
                            i["timestamp"] = int(timeParse(text).timestamp())
                        except Exception as e:
                            raise ParseError("time parse fail") from e
                case "link":
                    i["url"] = text or elem.get("href")
                case "name" if lastTag == "author":
                    i["author"] = text
                case "title":
                    i[tag] = text

            lastTag = tag

    if not items:
        raise ParseError("not valid result")

    feed = {
        "name": items[0]["title"],
        "lastupdate": items[0]["timestamp"],
        "items": items[1:]
    }

    return feed
