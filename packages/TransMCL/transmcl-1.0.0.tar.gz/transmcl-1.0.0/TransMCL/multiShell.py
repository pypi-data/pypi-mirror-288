from __future__ import print_function
import os
import sys
from multiprocessing import Process, Pool

def run(thread, commands):
    # print (thread, file=sys.stderr)
    for command in commands:
        pass
        # print (command, file=sys.stderr)
        os.system(command)

if __name__ == "__main__":
    if len(sys.argv)<3:
        print ( "python multiShell.py number_of_threads commands", file=sys.stderr)
        exit(0)
    
    threads = int(sys.argv[1])
    fileInput = open(sys.argv[2], "r")
    lines = []

    for line in fileInput:
        lines.append( line.strip() )
    
    part = max(1, len(lines) / threads)
    print ("commands [%d] === part [%d] === threads [%d]" % 
        (len(lines), part, threads),
        file=sys.stderr )

    pools = Pool(threads)
    for i in range(threads):
        if i<threads-1:
            pools.apply_async(run, args=( i, lines[i * part: (i+1)*part] ) )
        else:
            pools.apply_async(run, args=( i, lines[i * part:] ) )
    pools.close()
    pools.join()

    

    
