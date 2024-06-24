# rssfeed

A simple rss/atom feed parser

## Installation

`pip install rssfeed`

## Get Started

``` python
import requests
import rssfeed

feed = rssfeed.parse(requests.get("https://www.solidot.org/index.rss").text)
print(feed)
```
```
{
  "name": "奇客Solidot–传递最新科技情报",
  "lastupdate": 1717423475,
  "items": [
    {
      "title": "中国科学家使用细胞疗法治愈一名患者的糖尿病",
      "author": "",
      "timestamp": 1717410594,
      "url": "https://www.solidot.org/story?sid=78338",
      "content": "《南华早报》报道，中国科学家利用细胞疗法成功治愈了一名患者的糖尿病。研究报告发表在《Cell Discovery》期刊 ..."
    },
    {
      "title": "Steam 平台 Linux 玩家四分之三使用 AMD CPU",
      "author": "",
      "timestamp": 1717404736,
      "url": "https://www.solidot.org/story?sid=78337",
      "content": "根据 Valve 公布的 Steam 硬件和软件调查，Linux 份额在过去的五月增长了 0.42% 至 2.32%，macOS 增至 1.47% ..."
    },
    {
      "title": "Hugging Face 称黑客窃取了 Spaces 平台的身份验证令牌",
      "author": "",
      "timestamp": 1717400574,
      "url": "https://www.solidot.org/story?sid=78336",
      "content": "Hugging Face 官方博客披露黑客窃取了其 Spaces 平台的身份验证令牌。Spaces 是社区用户创建和递交 AI 应用的库 ..."
    }
    ...
  ]
}
```

## Warning

rssfeed **does not** escape any HTML tags, which mean if you does not check the content and display it somewhere html can be rendered, it may lead to [Cross-site scripting](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting) attacks.

## Changelog

[Changelog.md](/Changelog.md)

