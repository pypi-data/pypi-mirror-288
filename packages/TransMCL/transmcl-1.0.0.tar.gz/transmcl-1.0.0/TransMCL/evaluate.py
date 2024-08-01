from __future__ import print_function
import os
import sys
import json
import numpy as np
from alignment import *

level = { 
    "complete":0, 
    "incomplete":1, 
    "segment":2, 
    "chimera":3, 
    "redundent":4,
    None:5
}


def push_item(item, _map, _lst):
    if item in _map:
        return
    _map[item] = len(_lst)
    _lst.append(item)


def renew(_map, _link, key, value, link):
    # print ( key, value, link, _map[key], level[value], level[ _map[key]] )
    if level[value] < level[ _map[key] ]:
        _map[key] = value
        _link[key] = link


def evaluate_assembly(data, lengths, path=sys.stdout):

    # Initialize variables
    lines = []
    all_lst = [None]
    all_map = {}

    sam_set = set()
    sam_rec = {}
    std_set = set()
    std_rec = {}

    if path == sys.stdout:
        fp_eva = sys.stdout
        fp_sum = sys.stdout
    else:
        fp_eva = open(path + "_eva.txt", "w")
        fp_sum = open(path + "_sum.txt", "w")

    # Read aligment file
    for line in data:
        line_ = line.strip().split()
        
        # Keep unique hit for sample
        if len(all_lst)>1 and line_[0] == all_lst[lines[-1].qry]:
            pass
            continue

        # Ignore low quality alignment
        if float(line_[2])<90 and (float(line_[3])-float(line_[4])) / float(line_[3]) <.95:
            pass
            continue

        sam_set.add(line_[0])
        std_set.add(line_[1])

        push_item(line_[0], all_map, all_lst)
        push_item(line_[1], all_map, all_lst)
        lines.append( Alignment(line, all_map) )

    # Sort aligments by target gene
    lines.sort(key=lambda x: (x.tar, -x.bit))

    # Read length file
    gene_len = {}
    for line in lengths:
        line = line.strip().split()
        gene, length = line[0], line[1]
        if gene not in all_map: continue
        gene = all_map[gene]
        gene_len[gene] = int(length)

    # Print log information
    print ("Size of all: %d" % len(all_map), file=sys.stderr)
    print ("Size of sample: %d" % len(sam_set), file=sys.stderr)
    print ("Size of standard: %d" % len(std_set), file=sys.stderr)
    print ("Size of length: %d" % len(gene_len), file=sys.stderr)

    # Analysing result
    sam_rec = { all_map[it]:None for it in sam_set }
    sam_sum = {
        "complete":0,
        "incomplete":0,
        "segment":0,
        "chimera":0,
        "redundent":0
    }
    sam_link = {}
    
    std_rec = { all_map[it]:None for it in std_set }
    std_link = {}
    std_sum = {
        "complete":0,
        "incomplete":0,
        "segment":0,
        "chimera":0
    }
    

    i = 0
    j = 0
    while i<len(lines):

        # Get aligments targeted to same target gene
        j = i - 1
        while j+1<len(lines) and lines[j+1].tar == lines[i].tar: 
            j += 1

        # Check if chimera match
        line = lines[i]
        label = None
        if float(line.qrR-line.qrL+1) / gene_len[line.qry] < 0.8:
            label = "chimera"
        else:
            # Not chimera
            if float(line.taR-line.taL+1) / gene_len[line.tar] > 0.8:
                # complete match
                label = "complete"
            else:
                # incomplete match, check if segments exsits
                label = "incomplete"
                left = lines[i].taL
                right = lines[i].taR
                for k in range(i+1, j+1):
                    left = min( left, lines[k].taL )
                    right = max( right, lines[k].taR )
                dirta = (lines[i].taL - left) + (right - lines[i].taR)
                if dirta > 50 or float(dirta)/gene_len[lines[i].tar] > 0.1:
                    label = "segment"
            
        # Label algments
        renew(sam_rec, sam_link, line.qry, label, line.tar)
        renew(std_rec, std_link, line.tar, label, line.qry)
        for k in range(i+1, j+1):
            if label != "segment":
                renew(sam_rec, sam_link, lines[k].qry, "redundent", line.qry)
            else:
                renew(sam_rec, sam_link, lines[k].qry, "segment", line.tar)

        i = j+1

    # Print cleand aligments
    for idx, line in enumerate(lines):

        if idx==0 or idx>0 and line.tar>lines[idx-1].tar:
            std_sum[ std_rec[line.tar] ] += 1
            if idx and fp_eva: 
                print (file=fp_eva)
        sam_sum[ sam_rec[line.qry] ] += 1
        if not fp_eva: continue
        print (
            "%d\t[%s]\t%d\t[%s]\t%.1f\t%d\t%d\t%d\t[%d:%d]\t[%d:%d]\t%.2e\t%.1f\ttranscript:%s\tgenome:%s" % 
            (line.qry, all_lst[line.qry], 
            line.tar, all_lst[line.tar],
            line.idt, line.mat, line.mis, line.gap, 
            line.qrL, line.qrR, line.taL, line.taR, line.eva, line.bit,
            sam_rec[line.qry], std_rec[line.tar]),
            file=fp_eva
        )
    print ("Evaluation file:\t%s" % sys.argv[1], file=fp_sum)
    print (json.dumps(sam_sum), json.dumps(std_sum), sep="\n", file=fp_sum)
    for k, v in sorted(level.items(), key=lambda x: x[1]):
        if not k:
            continue
        print ( "%s\t%d\t%d" % 
            (k, std_sum.get(k, 0), sam_sum.get(k, 0) ),
            file = fp_sum 
        )
    

if __name__ == "__main__":
    if len(sys.argv)<4:
        print("python evaluate.py alignment_file length_file output_prefix", file=sys.stderr)
        exit()

    fileInput = open(sys.argv[1], "r")
    fileLength = open(sys.argv[2], "r")
    filePath = sys.argv[3]
    data = []
    lengths = []

    # Load files
    for line in fileInput:
        data.append( line.strip() )
    for line in fileLength:
        lengths.append( line.strip() )
    fileInput.close()
    fileLength.close()

    evaluate_assembly(data, lengths, filePath)
