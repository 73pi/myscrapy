# -*- coding: utf-8 -*-#

from time import sleep
import time
import threading

# 工作函数
def work(customer):
    print '消费者：', customer
    sleep(3)
    print '完成', customer

def developer_day(customers):
    lock = threading.Lock()
    def dev_day(id):
        print '早上好，', id
        lock.acquire()
        while customers:
            customer = customers.pop(0)
            lock.release()
            work(customer)
            lock.acquire()
        lock.release()
        print '完成', id

    devs = [threading.Thread(target=dev_day, args=(i,)) for i in range(5)]
    [dev.start() for dev in devs]
    [dev.join() for dev in devs]


start = time.time()
developer_day(["Customer %i" % i for i in xrange(15)])
end = time.time()
print end-start
