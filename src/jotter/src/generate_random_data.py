from __future__ import division

import time
import random
import sys
from datetime import datetime
from faker import Faker

fake = Faker()


def random_ping_message():
    if random.randint(0, 100) > 95:
        return "Request timed out.\n"
    else:
        return "Reply from %s: bytes=32 time=%sms TTL=60\n" % (random_ip(), random.randint(1, 100))


def random_stauts_code():
    x = random.randint(0, 10)

    if x <= 7:
        return 200
    elif x == 9:
        return 302

    return 500


def random_nginx_message(random_time=True):
    #95.108.214.16 - - [22/Sep/2013:03:53:44 +0400]  "GET /posts.rss HTTP/1.1" 200 110368 "http://tomforb.es/posts.rss" "Mozilla/5.0 (compatible; YandexBlogs/0.99; robot; B; +http://yandex.com/bots)1 readers" 0.420 0.002 .
    ip = fake.ipv4()
    if random_time:
        time_this_month = fake.date_time_this_month()
    else:
        time_this_month = datetime.now()
    method = "GET" if random.randint(0, 10) <= 9 else "POST"
    uri = "/%s" % fake.uri_path(random.randint(1, 5))
    code = random_stauts_code()
    response_size = random.randint(50, 1024*1024)
    referrer = fake.url()
    user_agent = fake.user_agent()
    response_time = round(random.random(), 3)

    return '%s - - [%s] "%s %s HTTP/1.1" %s %s "%s" "%s" %s 0' % (
        ip,
        time_this_month.strftime("%d/%b/%Y:%H:%M:%S +0000"),
        method,
        uri,
        code,
        response_size,
        referrer,
        user_agent,
        response_time
    )


def random_ip():
    return "%s.%s.%s.%s" % (random.randint(1, 255),
                            random.randint(1, 255),
                            random.randint(1, 255),
                            random.randint(1, 255))


def main():
    if sys.argv[1] == "ping":
        generator = random_ip
    else:
        generator = random_nginx_message


    for i in xrange(int(sys.argv[2])):
        print generator()


if __name__ == "__main__":
    main()