from dateutil.parser import parse as timeParse
from xml.etree import ElementTree

__version__ = "0.3"

def parse(data):
    assert type(data) == str, "data argument must be a string"
    if not data or not (data:=data.lstrip()):
        return
    if not any((data.startswith(i) for i in ("<?xml ", "<rss ", "<feed "))):
        return
    parser = ElementTree.XMLPullParser(("start", "end"))
    try:
        parser.feed(data)
        parser.close()
    except ElementTree.ParseError:
        return

    items = list()
    path = list()
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
            path.append(tag)
        else:
            match tag:
                case "summary" | "description" | "encoded":
                    tag = "content"
                case "updated" | "pubDate" | "published" | "lastBuildDate":
                    if text.isdigit():
                        items[-1]["timestamp"] = int(text)
                    elif text:
                        try:
                            items[-1]["timestamp"] = int(timeParse(text).timestamp())
                        except:
                            pass
                    continue
                case "link":
                    items[-1]["url"] = text or elem.get("href")
                    continue
                case "author":
                    authorTag = False
                    continue
                case "name" if path[-2] == "author":
                    tag = "author"
                case "title" | "content":
                    pass
                case _:
                    continue

            items[-1][tag] = text
            path.pop()

    if not items: return
    feed = {
        "name": items[0]["title"],
        "lastupdate": items[0]["timestamp"],
        "items": items[1:]
    }
    # for item in items:
    #     if feed["lastupdate"] < item["timestamp"]:
    #         feed["lastupdate"] = item["timestamp"]

    return feed

