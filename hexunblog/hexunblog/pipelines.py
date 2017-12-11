from hexunblog.items import HexunblogItem
from hexunblog.dao.database_connection import DBConnection


class HexunblogPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, HexunblogItem):
            conn = DBConnection.connect()
            with conn.cursor() as cursor:
                sql = "INSERT INTO articles(article_name,article_click_count,article_comment_count) VALUES (%s, %s, %s)"
                cursor.execute(sql, (item["article_name"], item["article_click_count"], item["article_comment_count"]))
                conn.commit()
            DBConnection.disconnect(conn)

