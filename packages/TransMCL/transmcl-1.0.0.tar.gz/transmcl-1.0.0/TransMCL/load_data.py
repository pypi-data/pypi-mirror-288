from __future__ import print_function
import os
import sys
import numpy as np
from .nwk import *
import subprocess



def load_info(file_input):
    """
        Gene_Number, BLAST_Number
        i, Gene_name
    """
    gene_lst = [[]]
    gene_map = {}

    line=file_input.readline()
    line=line.strip('\n').split('\t')
    N, M = int(line[0]), int(line[1])
    print (line[0]," genes,", line[1], " abc records", file=sys.stderr)
    for line in file_input:
        line=line.strip('\n').split('\t')
        gene_lst.append(line[1])
        gene_map[line[1]]=int(line[0])
    print ("Gene numbers:\t", len(gene_map), file=sys.stderr)
    return N, M, gene_lst, gene_map



def load_faa(file_input, gene_map):
    """
        Fasta format
    """
    gene_faa = [" " for i in range(len(gene_map)+1)]
    gene = None
    count = 0
    for i, line in enumerate(file_input):
        if (i+1) % 100000==0: 
            print (i+1, "FASTA lines read", file=sys.stderr)
            #return gene_faa
        line=line.strip().split()
        if line[0][0]==">" :
            gene = gene_map.get(line[0][1:], None)
            if gene: count += 1
        else:
            if not gene:
                continue
            # print ( line[0] )
            gene_faa[gene] += line[0]
    print ("FASTA numbers:\t", count, file=sys.stderr)
    return gene_faa



def load_len(file_input, gene_map):
    """
        Gene_name Gene_len
    """
    gene_len = {}
    
    for line in file_input:
        line=line.strip("\n").split("\t")
        if line[0] not in gene_map: continue
        x=gene_map[line[0]]
        gene_len[x]=int(line[1])
    print ("Length file size: ", len(gene_len), file=sys.stderr)
    return gene_len



def load_spe(file_input, gene_map):
    """
        Gene_name Gene_species
    """
    spe_lst = [""]
    spe_map = {}
    gene_spe = {}

    for line in file_input:
        line=line.strip("\n").split("\t")
        if line[0] not in gene_map: continue
        x=gene_map[line[0]]
        if line[1] not in spe_map:
            spe_map[line[1]]=len(spe_lst)
            spe_lst.append(line[1])
        gene_spe[x]=spe_map[line[1]]
    print ("Species file size: ", len(gene_spe), file=sys.stderr)
    print ("Species numbers:\t", len(spe_map), file=sys.stderr)

    return spe_lst, spe_map, gene_spe



def load_tra(file_input, spe_map):
    """
        List of species that is genome
    """
    spe_tra=[False for _ in range(len(spe_map)+1)]
    for line in file_input:
        line=line.strip('\n')
        if line in spe_map:
            spe_tra[spe_map[line]]=True
    # for x,species in enumerate(spe_map):
    #     print (spe_map[species], '\t',species, '\t', spe_tra[spe_map[species]])
    return spe_tra



def load_tre(file_input, spe_map, spe_lst, spe_tra):
    """
        Load species tree in Newick format
    """
    line=file_input.readline().strip("\n")
    spe_tre=Tree( len(spe_map), spe_map, spe_lst, spe_tra )
    spe_tre.load_nwk(line)
    spe_tre.print_tree(sys.stderr)
    spe_tre.find_guide_num(2)
    # spe_tre.find_guide_taxa()

    print("", file=sys.stderr)
    for species, guideSpecies in enumerate(spe_tre.guide):
        if spe_tra[species]:
            print ("guide species for %s:\t\t%s" % 
                (spe_lst[species], ", ".join(map( lambda x: spe_lst[x], guideSpecies )) ), 
                file=sys.stderr )
    print("", file=sys.stderr)

    return spe_tre



def load_mcl(file_input, file_output, spe_tre, spe_tra, gene_map, gene_spe, gene_len):
    """
        Load tabular MCL result
    """
    #print (spe_tre)
    file_output = open( file_output+"/mcl_info.txt", "w" )

    gene_grp = {}
    mcl_list = [[]]
    mcl_parm = [[]]

    for x, line in enumerate(file_input):
        line=line.strip('\n').split('\t')
        mcl_list.append([])
        spe_set=set()
        lens = []
        
        for gene in line:
            if gene not in gene_map:
                print ("\terror: ", gene, " is not supplied in the info file")
            else:
                gene_id=gene_map[gene]
                gene_grp[gene_id]=x+1
                mcl_list[x+1].append(gene_id)
                spe_set.add(gene_spe[gene_id])
                # Only count gene length from annotated genome
                if not spe_tra[ gene_spe[gene_id] ]:
                    lens.append(gene_len[gene_id])

        lca=spe_tre.lca(list(spe_set))
        mcl_parm.append([ len(mcl_list[x+1]), len(spe_set), lca])
        if lens:
            mcl_parm[-1].append(np.median(lens))
        else:
            mcl_parm[-1].append(-1.)
        print (x+1, len(mcl_list[x+1]), len(spe_set), lca, mcl_parm[-1][-1], file=file_output)
        print ("\t%s" % str(lens), file=file_output)

    print ("MCL groups:", len(mcl_list)-1, file=sys.stderr )
    file_input.close()

    return gene_grp, mcl_list, mcl_parm



def load_rlt(file_input, N):
    """
        Load isoform relations
        Transcript_i Transcript_i's isoform
    """
    gene_rlt=[i for i in range(N+1)]
    #print ('Gene relation size:', len(gene_rlt)-1)
    for line in file_input:
        #print (line)
        line=line.strip('\n').split('\t')
        gene_rlt[int(line[0])]=int(line[1])
    return gene_rlt



def load_abc(file_input, file_output, gene_map, gene_lst, gene_grp, gene_spe, spe_tra):
    """
        Drop orphan genes in complete OGs
    """

    def deal_blast(gene, arr):
        out = []
        for k, v in arr.items():
            # v = np.array(v)
            # out.append([k, np.sum(v), np.average(v)])
            # if len(v)>1 or True:
            #     pass
            #     print ('paralog', k, v)
            out.append([ k, v[0], v[0]/v[1] ])
        out.sort(key=lambda x: -x[2])
        ans = []
        for i, (k, sum_, ave_,) in enumerate(out):
            if (i==5 or ave_<out[0][2]*0.9) and k!=gene_grp[gene]:
                # return out[:i]
                continue
            ans.append([ k, sum_, ave_ ])
        return ans

    gene_ass = {}
    temp = {}
    last_gene = None

    # If gene_ass already exsit
    try:
        file_output = open( file_output+"/gene_assign.txt", "r" )
    except IOError:

        for x, line in enumerate(file_input):
            if x % 1000000 ==0:
                print ("%d lines of abc read" % (x+1), file=sys.stderr)
            line = line.strip().split()
            gene0, gene1 = int(line[0]), int(line[1])
            group0, group1 = gene_grp[gene0], gene_grp[gene1]
            
            if spe_tra[ gene_spe[gene0] ] == False:
                continue
            if spe_tra[ gene_spe[gene1] ] == True:
                continue
            if gene0==None or gene1==None:
                print ("line", x, "BLAST is illeagal")
                continue

            if last_gene!=None and gene0!=last_gene:
                gene_ass[last_gene] = deal_blast(last_gene, temp)
                temp = {}

            if group1 in temp:
                # temp[group1].append(float(line[-1]))
                temp[group1][0] += float(line[-1])
                temp[group1][1] += 1.
            else:
                # temp[group1] = [float(line[-1])]
                temp[group1] = [ float(line[-1]), 1. ]

            last_gene = gene0
        gene_ass[last_gene] = deal_blast(last_gene, temp)

        file_output = open( file_output+"/gene_assign.txt", "w" )
        
        for gene, assign in sorted(gene_ass.items(), key=lambda x: (x[0])):
            print (gene, gene_lst[gene], gene_grp[gene], sep="\t", file=file_output)
            for item in assign:
                print ("\t%d\t%.1f\t%.1f" % (item[0], item[1], item[2]), file=file_output)
            print ("", file=file_output)

        file_output.close()
        return gene_ass
        
    else:
        for idx, line in enumerate(file_output):
            line = line.rstrip().split("\t")

            if  len(line)==1:
                continue
            if line[0]:
                last_gene = gene_map.get( line[1], None)
            else:
                if not last_gene:
                    continue
                group, sum_, ave_ = int(line[1]), float(line[2]), float(line[3])
                if last_gene not in gene_ass:
                    gene_ass[last_gene] = [ [group, sum_, ave_] ]
                else:
                    gene_ass[last_gene].append([ group, sum_, ave_ ])
        print ("original gene_ass %d" % len(gene_ass), file=sys.stderr)
        file_output.close()
        return gene_ass



def load_blast(file_input, file_output, gene_map, gene_grp, gene_ass, gene_spe, spe_tra, spe_tre):

    try:
        os.system("rm  " + file_output + "/splitBlast/*" )
    except Exception:
        pass

    for i, line in enumerate(file_input):
        line_ = line.strip('\n').split()
        gene0, gene1 = gene_map.get(line_[0], None), gene_map.get(line_[1], None)
        
        if gene0==None or gene1==None: continue
        spe0, spe1 = gene_spe[gene0], gene_spe[gene1]
        if not (spe_tra[spe0] and spe1 in spe_tre.guide[spe0]):
            continue

        # if gene_grp[gene0] == gene_grp[gene1]:
        #     file_out = open(file_output+"_splitBlast/group_"+str(gene_grp[gene0]), "a")
        #     print (line, end="", file=file_out)
        #     file_out.close()

        groups0 = set()
        groups1 = set()
        groups0.add( gene_grp[gene0])
        groups1.add( gene_grp[gene1])
        if gene0 in gene_ass: 
            for it in gene_ass[gene0]:
                groups0.add(it[0])
        if gene1 in gene_ass: 
            for it in gene_ass[gene1]:
                groups1.add(it[0])

        intersection = groups0 & groups1
        if intersection:
            # print (line_, intersection, file=sys.stderr)
            for grp in intersection:
                # if grp == gene_grp[gene0]: continue
                file_out = open(file_output+"/splitBlast/group_"+str(grp), "a")
                print (line, end='', file=file_out)
                file_out.close()
