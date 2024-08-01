from __future__ import print_function
import os
import sys
from load_data import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

color = ["green", "orange", "grey"]
def draw_plot(data, intervals, fp="example.png"):
    
    fig, ax = plt.subplots()
    y = len(data)

    for i in range( len(data) ):

        # Decide color
        if data[i][0][:2] == "Al" or data[i][0][:2] == "Br":
            color = "blue"
        elif data[i][0][:2] == "Ah" or data[i][0][:2] == "Tp":
            color = "orange"
        else:
            color = "grey"

        # Draw interval
        for l, r in intervals[i]:
            plt.plot(
                [l+1, r+1], [y, y],
                color = color,
                linewidth = 2
            )
        if i>6:
            y -= .5
        else:
            y -= 1
    
    plt.xlabel("position")
    plt.ylabel("sequence")
    # plt.yticks([])
    # plt.ylim(ymax=y, ymin=2)
    plt.title("-")
    plt.legend(loc="upper right")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


     #plt.show()
    plt.savefig(fp)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv)<3:
        print ("python deal_msa.py raw_file fasta_file output_prefix msa")
        exit()
    
    # For group 768
    order = {
        "Alyrata_35939658" : 1,
        "Ahalleri_28854577" : 2,
        "Alyrata_35935900" : 3,
        "Ahalleri_28860536" : 4,
        "Alyrata_35947419" : 5,
        "Alyrata_35939498" : 6, 
        "Ahalleri_28853424" : 7,
    }
    
    file_raw = open( sys.argv[1], "r")
    file_fasta = open(sys.argv[2], "r")
    output_prefix = sys.argv[3]

    # Load raw
    names = set()
    count = 0
    for line in file_raw:
        line = line.strip().split()
        qry = line[1][1:-1]
        tar = line[4][1:-1]

        names.add(qry)
        names.add(tar)

        if qry not in order:
            count += 1
            order[qry] = count
        order[tar] = -1
    file_raw.close()

    # Order

    
    # Load fasta
    flag = False
    fasta = []
    for line in file_fasta:
        line = line.strip()
        if line[0] == ">":
            flag = line[1:] in names
            if flag:
                fasta.append([ line[1:], "" ])
        else:
            if flag:
                fasta[-1][1] += line
    file_fasta.close()
    fasta.sort(key=lambda x: order[x[0]])

    # Write fasta
    file_out = open( output_prefix + ".fa", "w")
    for it in fasta:
        print (">%s\n%s" %(it[0], it[1]), file=file_out)
    file_out.close()

    # muscle
    os.system(
        "clustalo" + " --in " + output_prefix + ".fa" + \
        " --out " + output_prefix + ".msa" + \
        " --force " + \
        # " -matrix 0311/matrix" 
        ""
    )
    # clustalo
    os.system(
        "muscle" + " -in " + output_prefix + ".fa" + \
        " -out " + output_prefix + ".msa" + \
        # " -matrix 0311/matrix" + \
        ""
    )

    # Read MSA
    data = []
    file_input = open(output_prefix + ".msa", "r")
    for line in file_input:
        line = line.strip()
        if line[0] == ">":
            data.append([ line[1:], "" ])
        else:
            data[-1][1] += line
    file_input.close()

    # raxmlHPC-PTHREADS-SSE3 -s seq_msa.txt -n seq_tree.txt -m PROTCATJTT -f a -N 100 -x 1 -p 1 -T 8
    data.sort(key=lambda x: order[x[0]])
    intervals = []

    # Wirte msa intervals
    file_out = open( output_prefix + ".txt", "w")
    for idx, item in enumerate(data):
        print (item[0], file=file_out )
        # print (item[1][:10])

        intervals.append([])
        l = 0
        while l < len(item[1]):
            if item[1][l] != "-":
                r = l-1
                while r+1 < len(item[1]) and item[1][r+1]!= "-":
                    r += 1
                intervals[-1].append([l, r])
                l = r
            l += 1
        
        print ("\t%s" % str(intervals[-1]), file=file_out)
    
    draw_plot(data, intervals, output_prefix + ".png")

