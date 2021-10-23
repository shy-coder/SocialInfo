import pymysql

class PmabcspiderPipeline:

    def __init__(self):
        self.connect = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='spider')
        self.cursor = self.connect.cursor()
        print("！！！！！！！！！！数据库连接成功！！！！！！！！！！")

    def process_item(self, item, spider):
        insert_sql = """insert into njjyfy(article_title,article_content,article_imgs,article_publish_time,article_href) VALUES (%s,%s,%s,%s,%s)"""
        self.cursor.execute(
            insert_sql,
            (item['title'], item['content'], item['img'], item['publish_time'], item["href"])
        )
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
        print("！！！！！！！！！！数据库关闭成功！！！！！！！！！！")