import feedparser
from datetime import datetime, timedelta

# RSS一覧
feeds = [
    {
        "category": "教育行政・DX",
        "name": "文部科学省",
        "url": "https://www.mext.go.jp/b_menu/houdou/rss.xml"
    },
    {
        "category": "ICT・AI",
        "name": "ITmedia",
        "url": "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml"
    },
    {
        "category": "ICT・AI",
        "name": "Impress Watch",
        "url": "https://www.watch.impress.co.jp/data/rss/1.0/ipw/feed.rdf"
    },
    {
        "category": "教育ICT",
        "name": "EdTechZine",
        "url": "https://edtechzine.jp/rss/index.xml"
    },
    {
        "category": "一般ニュース",
        "name": "NHK",
        "url": "https://www3.nhk.or.jp/rss/news/cat0.xml"
    }
]

# 注目キーワード
keywords = [
    "特別支援",
    "ICT",
    "AI",
    "GIGA",
    "教育",
    "端末",
    "DX",
    "生成AI",
    "学校",
    "インクルーシブ"
]

items = []
seen_titles = set()

# RSS取得
for feed in feeds:

    d = feedparser.parse(feed["url"])

    # 取得件数増加
    for entry in d.entries[:20]:

        title = entry.title.strip()

        # 重複除去
        if title in seen_titles:
            continue

        seen_titles.add(title)

        # 注目記事判定
        priority = any(
            keyword.lower() in title.lower()
            for keyword in keywords
        )

        # 日付
        date = datetime.min

        if "published_parsed" in entry and entry.published_parsed:
            date = datetime(*entry.published_parsed[:6])

        items.append({
            "title": title,
            "link": entry.link,
            "source": feed["name"],
            "category": feed["category"],
            "date": date,
            "priority": priority
        })

# 並び替え
# priority=True が先、その中で新しい順
items.sort(
    key=lambda x: (x["priority"], x["date"]),
    reverse=True
)

# 現在時刻
from datetime import datetime, timezone, timedelta
JST = timezone(timedelta(hours=9))
now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")

# HTML生成
html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>教育ICTニュース</title>

<style>

body {{
    font-family: sans-serif;
    font-size: 14px;
    margin: 10px;
    line-height: 1.5;
}}

h1 {{
    font-size: 20px;
    margin-bottom: 5px;
}}

h2 {{
    font-size: 16px;
    margin-top: 20px;
    border-bottom: 1px solid #ccc;
}}

.update {{
    color: gray;
    font-size: 12px;
    margin-bottom: 15px;
}}

ul {{
    padding-left: 18px;
}}

li {{
    margin-bottom: 10px;
}}

a {{
    text-decoration: none;
    color: black;
}}

a:hover {{
    text-decoration: underline;
}}

.source {{
    color: gray;
    font-size: 12px;
}}

</style>
</head>

<body>

<h1>教育ICTニュース</h1>

<div class="update">
最終更新: {now}
</div>

<h2>★ 注目ニュース</h2>
<ul>
"""

# 注目ニュース
for item in items:

    if item["priority"]:

        html += f"""
<li>
<a href="{item['link']}">
{item['title']}
</a>
<br>
<span class="source">
[{item['category']}] {item['source']}
</span>
</li>
"""

html += """
</ul>

<h2>最新ニュース</h2>
<ul>
"""

# 一般ニュース
for item in items:

    if not item["priority"]:

        html += f"""
<li>
<a href="{item['link']}">
{item['title']}
</a>
<br>
<span class="source">
[{item['category']}] {item['source']}
</span>
</li>
"""

html += """
</ul>

</body>
</html>
"""

# 保存
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html を更新しました")
