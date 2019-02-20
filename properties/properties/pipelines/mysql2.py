# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         mysql2
# Description:  
# Author:       73
# Date:         2019/2/20
#-------------------------------------------------------------------------------

from twisted.enterprise import adbapi


# 爬取数据写入数据库
class MysqlWriter(object):
    @classmethod
    def from_settings(cls, settings):
        conn_kwargs = dict(host=settings["MYSQL_HOST"],
                           db=settings["MYSQL_DATABASE"],
                           user=settings["MYSQL_USER"],
                           passwd=settings["MYSQL_PASSWORD"],
                           charset='utf8',
                           use_unicode=True,
                           connect_timeout=5
                           )
        dbpool = adbapi.ConnectionPool('MySQLdb', **conn_kwargs)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    @staticmethod
    def handle_error(failure):
        print failure

    @staticmethod
    def do_insert(tx, item):
        sql = """REPLACE INTO properties (url, title, comefrom) VALUES (%s,%s,%s)"""
        args = (
            item["url"][0][:100],
            item["title"][0][:30],
            item["comeFrom"][:30]
        )
        tx.execute(sql, args)
