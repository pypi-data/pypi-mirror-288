from __future__ import print_function
import os
import sys
from load_data import load_len

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Evaluation:

    def __init__(self, line, gene_map):
        # Column 1: query gene
        # Column 3: target gene
        # Column 4: identity
        # Column 5: match sites
        # Column 6: mismatch sites
        # Column 7: gap opens
        # Column 8: query interval 
        # Column 9: target interval 
        # Column 10: e-value
        # Column 11: bit scores
        # Column 12: query status
        # Column 13: target status
        
        qryInt = line[8].replace("[", "").replace("]", "").split(":")
        tarInt = line[9].replace("[", "").replace("]", "").split(":")
        if line[3][1:-1] not in gene_map:
            print ( line[3][1:-1], "===", line)
        self.qry = gene_map[ line[1][1:-1] ]
        self.tar = gene_map[ line[3][1:-1] ]
        self.idt = float( line[4] )
        self.mat = int( line[5] )
        self.mis = int( line[6] )
        self.gap = int( line[7] )
        self.qrL = int( qryInt[0] )
        self.qrR = int( qryInt[1] )
        self.taL = int( tarInt[0] )
        self.taR = int( tarInt[1] )
        self.eva = float( line[10] )
        self.bit = float( line[11] )
        self.qSt = line[12][ line[12].find(":")+1: ]
        self.tSt = line[13][ line[13].find(":")+1: ]

    def to_string(self, gene_lst):
        out = []
        out.append( gene_lst[ self.qry ] )
        out.append( gene_lst[ self.tar ] )
        out.append( str(self.idt) )
        out.append( str(self.mat) )
        out.append( str(self.mis) )
        out.append( str(self.gap) )
        out.append( str(self.qrL) )
        out.append( str(self.qrR) )
        out.append( str(self.taL) )
        out.append( str(self.taR) )
        out.append( str(self.eva) )
        out.append( str(self.bit) )
        out.append( "transcript:"+self.qSt )
        out.append( "genome:"+self.tSt )
        return "\t".join(out)

level = { 
    "complete":0, 
    "incomplete":1, 
    "segment":2, 
    "chimera":3, 
    "redundent":4,
    None:5
}

level_list = [
    "complete",
    "incomplete",
    "segment",
    "chimera",
    "redundent",
    "none"
]

def draw_plot_(length, original_alignment, clean_alignment, fp="example.png"):
    x1 = [20,50,100,150,200,300,400,600,1000]
    y1 = [1,2,3,4,5,6,7,8,9]  
    y1 = [1 for _ in range(9)]  
    y2 = [2 for _ in range(9)]
    # plt.figure(figsize=(8,4.9))
    plt.plot(x1, y1, 
        label = original_alignment[0].tar,
        color = "black",
        #marker = "+",
        linewidth = 2
    )
    plt.plot(x1, y2, 
        label = "$example$",
        color = "y",
        #marker = "+",
        linewidth = 2
    )
    plt.xlabel("number")
    plt.ylabel("time")
    plt.title("-")
    plt.legend()
    #plt.show()
    plt.savefig("example.png")

def draw_plot(gene_lst, length, original_alignment, clean_alignment, fp="example.png"):
    plt.figure(figsize=(8,4.9))
    if original_alignment:
        genome = original_alignment[0].tar
    else:
        genome = clean_alignment[0].tar
    plt.plot([1, length], [0, 0],
        label = gene_lst[genome],
        color = "black",
        linewidth = 2
    )

    pos = -0.9
    for record in original_alignment:
        
        pos -= 0.1
        plt.plot([record.taL, record.taR], [pos, pos], 
            #label = "original",
            color = "b",
            #marker = "+",
            linewidth = 2
        )
        pass

    pos -= 0.9
    for record in clean_alignment:
        
        pos -= 0.1
        plt.plot([record.taL, record.taR], [pos, pos], 
            #label = "clean",
            color = "g",
            #marker = "+",
            linewidth = 2
        )
        pass

    plt.xlabel("number")
    plt.ylabel("time")
    plt.title("-")
    plt.legend(loc="upper right")
    plt.ylim(ymax=1)
    #plt.show()
    plt.savefig(fp)
    plt.close()

def compare(file_original, file_clean, path_output, gene_map, gene_lst, gene_len):
    
    pass

    original_target = 0
    clean_target = 0
    records_original = [ [] for _ in range( len(gene_map)+1 )]
    records_clean = [ [] for _ in range( len(gene_map)+1 )]

    try:
        os.system("rm -rf " + path_output)
        os.system("mkdir " + path_output)
        os.system("mkdir " + path_output + "/figs")
    except Exception as e:
        pass
    file_output = open( path_output + "/logs.txt", "w")

    for line in file_original:
        line = line.strip().split()
        if not len(line):
            continue
        record = Evaluation(line, gene_map)
        if not records_original[ record.tar ]:
            original_target += 1
        records_original[ record.tar ].append(record)

    for line in file_clean:
        line = line.strip().split()
        if not len(line):
            continue
        record = Evaluation(line, gene_map)
        if not records_clean[ record.tar ]:
            clean_target += 1
        records_clean[ record.tar ].append(record)

    intersection = 0
    union = 0
    for i in range(1, len(gene_map)+1 ):
        len_original = len(records_original[i])
        len_clean = len(records_clean[i])
        if len_original and len_clean:
            intersection += 1
        if len_original or len_clean:
            union += 1
            level_original = 5
            level_clean = 5
            if len(records_original[i]):
                level_original = level[ records_original[i][0].tSt ]
            if len(records_clean[i]):
                level_clean = level[ records_clean[i][0].tSt ]
            if level_original != level_clean:
                if level_original > level_clean:
                    status = "better"
                else:
                    status = "worse"
                print ("%d [%s] len[%d] === %d[%s] %d[%s] === %s" 
                    % (i, gene_lst[i],  gene_len[i],
                    level_original, level_list[level_original],
                    level_clean, level_list[level_clean],
                    status),
                    file=file_output
                )
                for record in records_original[i]:
                    print ("\t%s" % record.to_string(gene_lst), file=file_output)
                print ("\t%s" % ("-" * 76), file=file_output)
                for record in records_clean[i]:
                    print ("\t%s" % record.to_string(gene_lst), file=file_output)
                print ("=" * 80, file=file_output)
                fp = path_output + "/figs/" + "gene_" + str(i) + ".png" 
                draw_plot(gene_lst, gene_len[i], records_original[i], records_clean[i], fp)

        
    print ("interseciont [%d]" % intersection, file=sys.stderr)
    print ("union [%d]" % union, file=sys.stderr)
    print ("original [%d]" % original_target, file=sys.stderr)
    print ("clean [%d]" % clean_target, file=sys.stderr)

    file_output.close()
    


if __name__ == '__main__':

    # draw_plot_(None, None, None)
    # exit()

    if len(sys.argv)<4:
        print("python interval.py original_eva clean_eva len_file output_dir", file=sys.stderr)
        exit()
    
    file_original = open(sys.argv[1], "r")
    file_clean = open(sys.argv[2], "r")
    file_len = open(sys.argv[3], "r")

    # Load gene map
    gene_map = {}
    gene_lst = [ None ]
    gene_set = set()
    for line in file_original:
        line = line.strip().split()
        if not line:
            continue
        gene_set.add( line[1][1:-1] )
        gene_set.add( line[3][1:-1] )
    for line in file_clean:
        line = line.strip().split()
        if not line:
            continue
        gene_set.add( line[1][1:-1] )
        gene_set.add( line[3][1:-1] )
    file_original.seek(0)
    file_clean.seek(0)

    for it in gene_set:
        gene_map[it] = len(gene_map) + 1
        gene_lst.append(it)

    # Load gene length
    gene_len = load_len(file_len, gene_map)

    # Print log
    print("gene_map size [%d] === gene_len size [%d]" % 
        ( len(gene_map), len(gene_len) ), file=sys.stderr
    )
    for it in gene_map.keys():
        it = gene_map[it]
        if it not in gene_len:
            print ("gene [%s]%d has no length info" % (gene_lst[it], it), file=sys.stdout)
    
    compare(file_original, file_clean, sys.argv[4], gene_map, gene_lst, gene_len)
    exit()
