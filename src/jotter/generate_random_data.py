import random
import sys

def random_ip():
    return "%s.%s.%s.%s" % (random.randint(1, 255),
                            random.randint(1, 255),
                            random.randint(1, 255),
                            random.randint(1, 255))

for i in xrange(int(sys.argv[1])):
    if random.randint(0, 100) > 95:
        sys.stdout.write("Request timed out.\n")
    else:
        sys.stdout.write("Reply from %s: bytes=32 time=%sms TTL=60\n" % (random_ip(), random.randint(1, 100)))