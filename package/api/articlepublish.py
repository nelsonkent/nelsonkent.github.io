# -*- coding: utf-8 -*-
# https://doocs.github.io/md/
# https://github.com/nelsonkent/wechat-mp-article
import datetime
import requests
import json


import requests
from bs4 import BeautifulSoup
def extract_article_from_webpage(url):
    # 发送 HTTP GET 请求获取页面内容
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve webpage: {url}")
        return None

    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到所有的 news-date 标签
    news_dates = soup.find_all(class_='news-date')

    if len(news_dates) < 2:
        print("Not enough news-date elements found")
        return None

    # 获取第一个和第二个 news-date 之间的文章内容
    first_news_date = news_dates[0]
    second_news_date = news_dates[2]

    # 找到第一个 news-date 后面的所有兄弟节点，直到第二个 news-date
    article_parts = []
    current_node = first_news_date.next_sibling
    while current_node and current_node != second_news_date:
        print(current_node)
        if hasattr(current_node, 'text'):
            replace = current_node.text.strip().split("\n")
            if len(replace) < 2:
                current_node = current_node.next_sibling
                continue
            article_parts.append('''<h1 style="text-align:center;line-height:1.75;font-family:-apple-system-font,BlinkMacSystemFont, Helvetica Neue, PingFang SC, Hiragino Sans GB , Microsoft YaHei UI , Microsoft YaHei ,Arial,sans-serif;font-size:1.2em;font-weight:bold;display:table;margin:0 auto;padding:0 1em;border-bottom:2px solid rgba(15, 76, 129, 1);color:#3f3f3f;margin-top: 0">'''+replace[0]+'''</h1>
    <p style="text-align:left;line-height:1.75;font-family:-apple-system-font,BlinkMacSystemFont, Helvetica Neue, PingFang SC, Hiragino Sans GB , Microsoft YaHei UI , Microsoft YaHei ,Arial,sans-serif;font-size:14px;margin:0 0 20px 0;letter-spacing:0.1em;color:#3f3f3f">'''+replace[1]+''''</p>
    ''')
            # print(current_node.)
            # article_parts.append()
        current_node = current_node.next_sibling

    # 将文章内容合并为字符串
    article_text = '<br/>'.join(article_parts)

    return article_text

# 指定页面 URL
url = "https://ai-bot.cn/daily-ai-news/"

# 调用函数提取文章内容
extracted_article = extract_article_from_webpage(url)

if extracted_article:
    print("提取的文章内容：")
    print(extracted_article)
else:
    print("未能成功提取文章内容")




def publish_article(access_token, article_data):
    access_token = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx9a5519171ae30eca&secret=61b3d44fb8c93b876e146111a407fb15").json().get('access_token')
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "articles": [article_data]
    }
    response = requests.post(url, headers={'Content-Type': 'application/json; charset=utf-8'
                                           }, data=bytes(json.dumps(data, ensure_ascii=False).encode('utf-8')))
    return response.json()



# 获取当前日期
current_date = datetime.date.today()

# 将日期格式化为指定格式的字符串
formatted_date = current_date.strftime("%Y-%m-%d")  # 格式化为 YYYY-MM-DD 的字符串
# 示例文章数据
article_data = {
    "title": "AI行业新鲜事：最新动向",
    "thumb_media_id": "4YwaNA4VnXHvAVu7105uPDmNVMbQMr31U0I_MsuUF8tWe58PTkv-oSShSMOPNg-m",
    "author": "科技谈",
    "content": '''<html><head><meta charset="utf-8" /></head><body><div style=" margin: auto;">
    <div style="text-align: center;"><img src="https://mmbiz.qpic.cn/sz_mmbiz_png/OZQ5KgG3b3y4EynQIbr88saG6dofnfQkmer4IVl8nUwrq6Lpfk2L7Osj6E5iaxYnZZR6nVvWhCly8RPX7r8k8icQ/640"style="width: 100%; height: auto; margin-top: 0;"></div>
    '''+extracted_article+'''<h4 style="text-align:left;line-height:1.75;font-family:-apple-system-font,BlinkMacSystemFont, Helvetica Neue, PingFang SC, Hiragino Sans GB , Microsoft YaHei UI , Microsoft YaHei ,Arial,sans-serif;font-size:1em;font-weight:bold;margin:2em 8px 0.5em;color:rgba(15, 76, 129, 1)">推荐阅读</h4><hr style="text-align:left;line-height:1.75;font-family:-apple-system-font,BlinkMacSystemFont, Helvetica Neue, PingFang SC, Hiragino Sans GB , Microsoft YaHei UI , Microsoft YaHei ,Arial,sans-serif;font-size:14px;border-style:solid;border-width:1px 0 0;border-color:rgba(0,0,0,0.1);-webkit-transform-origin:0 0;-webkit-transform:scale(1, 0.5);transform-origin:0 0;transform:scale(1, 0.5)"><p style="text-align:left;line-height:1.75;font-family:-apple-system-font,BlinkMacSystemFont, Helvetica Neue, PingFang SC, Hiragino Sans GB , Microsoft YaHei UI , Microsoft YaHei ,Arial,sans-serif;font-size:14px;margin:1.5em 8px;letter-spacing:0.1em;color:#3f3f3f">欢迎关注我的公众号“<strong style="text-align:left;line-height:1.75;color:rgba(15, 76, 129, 1);font-weight:bold">AI科技谈</strong>”，原创技术文章第一时间推送。</p><center>
    <img src="https://mmbiz.qpic.cn/sz_mmbiz_jpg/OZQ5KgG3b3y4EynQIbr88saG6dofnfQkM2j4SeIxoJ4maicbBuTxvJVMNyVf0PUbFbVewUcA8g2YkpWNeVvHcVQ/640" style="width: 100px;">
</center>
        </div></body></html>''',
    "digest": "AI行业新鲜事：最新动向" + formatted_date
}

# 替换为你的Access Token
access_token = "79_9SuN7T2DA_ps4I8-isq9LuSBxr-ef3GtQiKPbim1JX5JFR8JM62AednlmGLHJzhVfYZuMPwQe0a_NjcFtuSYk4UxVx7Vgrt4ElBWHHCW6tC5JProtumWXXMfR10EAOeAHAAWK"

# 发布文章
result = publish_article(access_token, article_data)
print(result)
