# -*- coding: utf-8 -*-#

import time
from twisted.internet import reactor, defer, task


# 工作函数
def work(customer):
    def schedule_work():
        def on_done():
            print 'callback:完成', customer
        print 'schedule:服务', customer
        return task.deferLater(reactor, 3, on_done)

    def all_done(_):
        print "全部完成", customer

    d = schedule_work()
    d.addCallback(all_done)
    return d


def twisted_developer_day(customers):
    print '早上好'
    works = [work(customer) for customer in customers]
    join = defer.DeferredList(works)
    join.addCallback(lambda _: reactor.stop())
    print '再见了各位'


start = time.time()
twisted_developer_day(["Customer %i" % i for i in xrange(15)])
reactor.run()
end = time.time()
print end-start
