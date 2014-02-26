import time
import sys
import os

#Set the filename and open the file
filename = sys.argv[-1]
with open(filename, "r") as fd:
    #Find the size of the file and move to the end
    st_results = os.stat(filename)
    st_size = st_results[6]
    fd.seek(st_size)
    i = 0

    while 1:
        where = fd.tell()
        line = fd.readline()
        if not line:
            time.sleep(1)
            fd.seek(where)
        else:
            print line,  # already has newline
            sys.stdout.flush()

            i += 1
            if i == 5:
                sys.exit()