# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import traceback
import MySQLdb

from twisted.internet import defer
from twisted.enterprise import adbapi


# 爬取数据写入数据库
class MysqlWriter(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def __init__(self):
        # Report connection error only once
        self.report_connection_error = True

        # Parse MySQL URL and try to initialize a connection
        conn_kwargs = dict(host='localhost',
                           db='properties',
                           user='root',
                           passwd='950210',
                           charset='utf8',
                           use_unicode=True,
                           )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **conn_kwargs)

    def close_spider(self, spider):
        self.dbpool.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        logger = spider.logger

        try:
            yield self.dbpool.runInteraction(self.do_replace, item)
        except MySQLdb.OperationalError:
            if self.report_connection_error:
                logger.error("Can't connect to MySQL" )
                self.report_connection_error = False
        except:
            print traceback.format_exc()

        # Return the item for the next stage
        defer.returnValue(item)

    @staticmethod
    def do_replace(tx, item):
        sql = """REPLACE INTO properties (url, title, comefrom) VALUES (%s,%s,%s)"""
        args = (
            item["url"][0][:100],
            item["title"][0][:30],
            item["comeFrom"][:30]
        )
        tx.execute(sql, args)
