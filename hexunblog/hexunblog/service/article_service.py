import requests
import re

from hexunblog.util.headers_util import HeadersUtil


class ArticleService(object):
    '''
    获得指定博文的评论数和点击量
    '''

    @classmethod
    def get_count(cls, response):
        headers = HeadersUtil.get_article_headers()
        headers["Referer"] = response.meta["url"]
        param = re.findall(r'cache-sidebar.blog.hexun.com/inc/ARecommend.aspx(.*?)&t=2', response.body.decode("gbk"))[0]
        url = "http://click.tool.hexun.com/click.aspx" + param.replace("articleids", "articleid")
        res = requests.get(url=url, headers=headers)
        # 获取点击量
        article_click_count = re.findall(r'\("articleClickCount"\).innerHTML = (.*?);', res.text)
        # 获取评论数
        article_comment_count = re.findall(r'\("articleCommentCount"\).innerHTML = (.*?);', res.text)
        return article_click_count, article_comment_count
