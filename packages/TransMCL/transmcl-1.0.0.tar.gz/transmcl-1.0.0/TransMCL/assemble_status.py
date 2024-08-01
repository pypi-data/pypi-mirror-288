from __future__ import print_function
import sys
import json

def plus(dict_, key_):
    if key_ in dict_:
        dict_[key_] += 1
    else:
        dict_[key_] = 1

def deal(data):

    global status
    global paralog_OG
    global paralog_gene
    global paralog_OGs
    global paralog_genes
    temp = {}

    for item in data:
        result = item[1].split(":")[1]
        plus(temp, result)
        plus(status, result)
    if temp.get("complete", 0) > 1:
        paralog_OG += 1
        paralog_gene += temp["complete"]
        paralog_OGs.append(data[0][3])
        for it in data:
            if it[1].split(":")[1] != "complete":
                continue
            paralog_genes.append([ it[0], it[3] ])


if __name__ == "__main__":
    if len(sys.argv)<3:
        print ("python assemble_status.py input_file output_file")
        exit()

    file_input = open( sys.argv[1], "r")
    file_output = open( sys.argv[2], "w")

    data = []
    status = {}
    paralog_OG = 0
    paralog_gene = 0
    paralog_OGs = []
    paralog_genes = []

    for line in file_input:
        line = line.strip().split()
        if data!=[] and line[3] != data[0][3]:
            deal(data)
            data = []
        data.append(line)
    deal(data)
    
    # print ("paralog OG: %d" % paralog_OG, file=sys.stderr)
    # print ("paralog gene: %d" % paralog_gene, file=sys.stderr)
    # print ("%s" % json.dumps(status), file=sys.stderr)

    print ("evaluation file:", file_input, file=file_output)
    print ("paralog OG: %d" % paralog_OG, file=file_output)
    print ("paralog gene: %d" % paralog_gene, file=file_output)
    print ("%s" % json.dumps(status), file=file_output)
    for OG in paralog_OGs:
        print (OG, file=file_output)
    
    for gene, OG in paralog_genes:
        print (gene, OG, file=file_output)
