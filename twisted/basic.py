# -*- coding: utf-8 -*-#

from time import sleep
import time

# 工作函数
def work(customer):
    print '消费者：', customer
    sleep(3)
    print '完成', customer

def developer_day(customers):
    for customer in customers:
        work(customer)


start = time.time()
developer_day(["张三","李四","王五","刘六"])
end = time.time()
print end-start
