from dateutil.parser import parse as timeParse
from xml.etree import ElementTree

__version__ = "0.2"

def parse(data):
    if not data or not (data:=data.lstrip()):
        return
    if not any((data.startswith(i) for i in ("<?xml ", "<rss ", "<feed "))):
        return
    parser = ElementTree.XMLPullParser(("start", "end"), _parser=ElementTree.XMLParser(encoding='utf-8'))
    try:
        parser.feed(data)
        parser.close()
    except ElementTree.ParseError:
        return

    items = list()
    authorTag = False
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
            elif tag == "author":
                authorTag = True
        else:
            match tag:
                case "guid":
                    tag = "id"
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
                    items[-1]["url"] = elem.get("href") if text and elem.get("href") else text
                    continue
                case "author":
                    authorTag = False
                    continue
                case "name" if authorTag:
                    tag = "author"
                case "title" | "id" | "content":
                    pass
                case _:
                    continue

            items[-1][tag] = text

    if not items: return
    feed = items.pop(0)
    feed = {
        "name": feed["title"],
        "lastupdate": feed["timestamp"],
        "items": items
    }
    for item in items:
        if item.get("id"):
            if not item["url"] and item["id"].startswith("http"):
                item["url"] = item["id"]
            del item["id"]

        if feed["lastupdate"] < item["timestamp"]:
            feed["lastupdate"] = item["timestamp"]

    return feed

