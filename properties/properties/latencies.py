# -*- coding: utf-8 -*-

from time import time
from scrapy.exceptions import NotConfigured
from twisted.internet import task
from scrapy import signals

# 测量吞吐量和延时 命令：scrapy crawl easy -s CLOSESPIDER_ITEMCOUNT=100 -s LOG_LEVEL=INFO
class Latencies(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        self.interval = crawler.settings.getfloat('LATENCIES_INTERVAL')

        if not self.interval:
            raise NotConfigured

        # connect the extension object to signals
        cs = crawler.signals.connect
        cs(self.spider_opened, signal=signals.spider_opened)
        cs(self.spider_closed, signal=signals.spider_closed)
        cs(self.request_scheduled, signal=signals.request_scheduled)
        cs(self.response_received, signal=signals.response_received)
        cs(self.item_scraped, signal=signals.item_scraped)
        self.latency, self.proc_latency, self.items = 0, 0, 0

    def spider_opened(self, spider):
        self.task = task.LoopingCall(self._log, spider)
        self.task.start(self.interval)

    def spider_closed(self, spider, reason):
        if self.task.running:
            self.task.stop()

    def request_scheduled(self, request, spider):
        request.meta['schedule_time'] = time()

    def response_received(self, response, request, spider):
        request.meta['received_time'] = time()

    def item_scraped(self, item, response, spider):
        self.latency += time() - response.meta['schedule_time']
        self.proc_latency += time() - response.meta['received_time']
        self.items += 1

    def _log(self, spider):
        irate = float(self.items)/self.interval
        latency = self.latency/self.items if self.items else 0
        proc_latency = self.proc_latency/self.items if self.items else 0
        spider.logger.info(("Scraped %d items at %.1f item/s, avg latency:"
                            "%.2f s and avg time in pipelines:%.2f s") %
                           (self.items, irate, latency, proc_latency))
        self.latency, self.proc_latency, self.items = 0, 0, 0


