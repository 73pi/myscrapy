# -*- coding: utf-8 -*-#

import time
from twisted.internet import reactor, defer, task


# 工作函数
@defer.inlineCallbacks
def inline_work(customer):
    print 'schedule:服务', customer
    yield task.deferLater(reactor, 3, lambda: None)
    print 'callback:完成', customer
    print "全部完成", customer


def twisted_developer_day(customers):
    print '早上好'
    # worksi改列表为元组
    works = (inline_work(customer) for customer in customers)
    # 设置并发限制coop，并发为5
    coop = task.Cooperator()
    join = defer.DeferredList([coop.coiterate(works) for i in xrange(5)])
    join.addCallback(lambda _: reactor.stop())
    print '再见了各位'


start = time.time()
twisted_developer_day(["Customer %i" % i for i in xrange(15)])
reactor.run()
end = time.time()
print end-start
