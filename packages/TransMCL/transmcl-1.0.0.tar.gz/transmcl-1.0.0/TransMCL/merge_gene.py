from __future__ import print_function
import os
import sys
import numpy as np
from .alignment import *
from .network import Maxmium_Flow, Eliminate_Circle
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

fileLog = None
fileFaa = None
merged_faa = None
netflow_faa = None
output_item = None
merged_coo = None
output_list = []

def dist_custom(vec1, vec2):
    if vec1[0]<vec2[0]:
        return vec2[0]-vec1[1]
    else:
        return vec1[0]-vec2[1]


def merge_faa(vecs_lst, vecs_src, data, item_lst, gene_faa, gene_lst):

    global output_item
    global output_list

    id_ = lambda x: item_lst[ vecs_lst[x] ]
    target = lambda x: data[vecs_src[x][1]].tar
    qryInterval = lambda x: ( data[x].qrL, data[x].qrR )
    tarInterval = lambda x: ( data[x].taL, data[x].taR )
    output_list = []
    fasta = gene_faa[ id_(0) ][ qryInterval(vecs_src[1][0])[0]: qryInterval(vecs_src[1][0])[1]+1 ]

    #print("first:", qryInterval(vecs_src[1][0])[0], qryInterval(vecs_src[1][0])[1], sep = "\t", file = fileLog)
    #print("vecs_lst[x]:", vecs_lst[0], sep="\t", file=fileLog)
    #print("vecs_src[x]:", vecs_src[0], sep="\t", file=fileLog)

    #print the gene name
    output_item = [0, (gene_lst[id_(0)], id_(0)), (gene_lst[target(1)],target(1)), qryInterval(vecs_src[1][0]),tarInterval(vecs_src[1][0])]
    #output_dict[gene_lst[id_(0)]] = qryInterval(vecs_src[1][0])
    output_list.append([gene_lst[id_(0)], qryInterval(vecs_src[1][0]), 0])
    print ("", 0, id_(0), target(1), qryInterval(vecs_src[1][0]), tarInterval(vecs_src[1][0]), len(gene_faa[ id_(0) ])-1 , sep="\t", file=fileLog)

    for i in range(1, len(vecs_lst) ):
        print(vecs_lst, file=fileLog)
        print(vecs_src, file=fileLog)
        print ("", i, id_(i), target(i), qryInterval(vecs_src[i][1]), tarInterval(vecs_src[i][1]), len(gene_faa[ id_(i) ])-1 , sep="\t", file=fileLog)
        #print ("\t", data[ vecs_src[i]-1 ].qry, data[ vecs_src[i]-1 ].taR, qryInterval(vecs_src[i]-1), tarInterval(vecs_src[i]-1), sep="\t", file=fileLog)
        
        if tarInterval(vecs_src[i][1])[0]>tarInterval(vecs_src[i][0])[1]:        
            output_item = [str(i), (gene_lst[id_(i)], id_(i)), (gene_lst[target(i)], target(i)), (qryInterval(vecs_src[i][1])[0], qryInterval(vecs_src[i][1])[1]), (tarInterval(vecs_src[i][1])[0], tarInterval(vecs_src[i][1])[1])]
            #output_dict[gene_lst[id_(i)]] = (qryInterval(vecs_src[i][1])[0], qryInterval(vecs_src[i][1])[1])
            output_list.append([gene_lst[id_(i)], (qryInterval(vecs_src[i][1])[0], qryInterval(vecs_src[i][1])[1]), i])
            fasta += gene_faa[ id_(i) ][ qryInterval(vecs_src[i][1])[0]: qryInterval(vecs_src[i][1])[1]+1 ]
        else:            
            output_item = [str(i), (gene_lst[id_(i)], id_(i)), (gene_lst[target(i)], target(i)), (qryInterval(vecs_src[i][1])[0]+tarInterval(vecs_src[i][0])[1]-tarInterval(vecs_src[i][1])[0]+1, qryInterval(vecs_src[i][1])[1]), (tarInterval(vecs_src[i][1])[0], tarInterval(vecs_src[i][1])[1]) ]
            #output_dict[gene_lst[id_(i)]] = (qryInterval(vecs_src[i][1])[0]+tarInterval(vecs_src[i][0])[1]-tarInterval(vecs_src[i][1])[0]+1, qryInterval(vecs_src[i][1])[1])
            output_list.append([gene_lst[id_(i)], (qryInterval(vecs_src[i][1])[0]+tarInterval(vecs_src[i][0])[1]-tarInterval(vecs_src[i][1])[0]+1, qryInterval(vecs_src[i][1])[1]), i])
            fasta += gene_faa[ id_(i) ][ qryInterval(vecs_src[i][1])[0]+tarInterval(vecs_src[i][0])[1]-tarInterval(vecs_src[i][1])[0]+1 : qryInterval(vecs_src[i][1])[1]+1]
    return output_list, fasta


def deal_species_aligments(
    group,
    data_, 
    gene_map, 
    gene_lst, 
    gene_len, 
    gene_spe, 
    gene_faa, 
    spe_tra, 
    spe_tre, 
    mcl_parm
):
    
    pass

    global fileLog
    global fileFaa
    global merged_faa

    species = spe_tre.lst[ gene_spe[ data_[0].qry ] ]
    exclude = set()
    temp_rec = []

    # Sort according to target gene and targeted interval
    data = []
    data_.sort(key=lambda x: (x.tar, x.taL, -x.taR, -x.bit) )
    for item in data_:
        if len(data)==0:
            data.append(item)
        elif item.tar != data[-1].tar:
            data.append(item)
        elif item.taR > data[-1].taR:
            data.append(item)
    data = data_

    # Get map and list for transcripts
    item_map = {}
    item_lst = [None]
    for alignment in data:
        print ( "%d\t[%s]\t%d:%d]\t\t%d\t[%s]\t%d:%d]\t%.1f" % 
            ( alignment.qry, gene_lst[alignment.qry], alignment.qrL, alignment.qrR, 
            alignment.tar, gene_lst[alignment.tar], alignment.taL, alignment.taR, alignment.bit),
            file=fileLog
        )
        if alignment.qry not in item_map:
            item_map[alignment.qry] = len(item_lst)
            item_lst.append(alignment.qry)
    size = len(item_map)

    # Print log information
    print ("\tSize of transcripts: %d" % size, file=fileLog )
    dists = np.zeros((size+2, size+2), dtype=int)
    detail = {}

    # Skip condition
    if size==1:
        pass
        return set()

    # Get aligments interval for same target gene
    i = 0
    while i<len(data):

        vecs = []
        vecs_lst = []
        vecs_src = []
        j = i-1
        last = -1

        # Get alignments target to same guided gene
        while j+1<len(data) and data[j+1].tar == data[i].tar: 
            j += 1
            # exclude.add( data[j].qry )
            if vecs and data[j].taR<=vecs[-1][1]: 
                # continue
                pass
            vecs.append(np.array([ data[j].taL, data[j].taR ]))
            vecs_lst.append( item_map[ data[j].qry ] )
            vecs_src.append([last,j])
            last = j

        vecs = np.array(vecs)
        if len(vecs)>1:

            # Hierarchy clustering
            links = linkage(vecs, method="single", metric=dist_custom)

            # Pring log
            print ("\tIntervals%d:%d" % (i, j), file=fileLog)
            for idx, item in enumerate(vecs_lst):
                # if idx:
                #     pre = vecs_lst[idx-1]
                #     if vecs[idx-1][1] - vecs[idx][0] > 200 and vecs[idx][1]-vecs[idx-1][1]<vecs[idx-1][1] - vecs[idx][0]:
                #         continue
                #     dists[pre][item] += 1
                #     if (pre, item) not in detail:
                #         detail[ (pre, item) ] = [ vecs_src[idx] ]
                #     else:
                #         detail[ (pre, item)].append( vecs_src[idx] )
                print (
                    "", idx, item, gene_lst[item_lst[item]], vecs[idx], 
                    data[i+idx].mat, data[i+idx].mis, data[i+idx].gap,
                    data[i+idx].bit, data[i+idx].bit/(data[i+idx].qrR-data[i+idx].qrL),
                    sep="\t", file=fileLog
                )

            # Build network
            # if np.sum(dists, axis=0)[ vecs_lst[0] ] == 0:
            #     dists[0][ vecs_lst[0] ] = 1024
            # if np.sum(dists, axis=1)[ vecs_lst[-1] ] == 0:
            #     dists[ vecs_lst[-1], size+1 ] = 1024

            for x in range(i, j+1):
                pre = vecs_lst[x-i]
                bit_pre = data[x].bit/(data[x].qrR-data[x].qrL)
                edge = []

                for y in range(x+1, j+1):

                    cur = vecs_lst[y-i]

                    # Overlap
                    overlap = vecs[x-i,1] - vecs[y-i,0]
                    dirta = vecs[y-i,1] - vecs[x-i,1]
                    bit_cur = data[y].bit/(data[y].qrR-data[y].qrL)
                    if overlap>0 and overlap>dirta:
                        # continue
                        pass  

                    # Skip condition: overlaped seqs and similariy diffuse
                    # Change to SNP
                    if vecs[y-i][1]<=vecs[x-i][1]:
                        continue
                    if abs(bit_cur-bit_pre)>0.1 and float(vecs[x-i][1] - vecs[y-i][0] ) / (vecs[x-i][1]-vecs[x-i][0]) > 0.5:
                        continue
                    if abs(bit_cur-bit_pre)>0.1 and float(vecs[x-i][1] - vecs[y-i][0] ) / (vecs[y-i][1]-vecs[y-i][0]) > 0.5:
                        continue


                    if len(edge)==0:
                        edge = [y, cur, bit_cur]
                    elif vecs[y-i][0]>=vecs[ edge[0]-i ][1]:
                        break
                    # Renew condition: better average bit score while potential seqs overlaped
                    elif abs(edge[2]-bit_pre)>0.1 and abs(bit_cur-bit_pre) < abs( edge[2]-bit_pre ) and \
                        ( float( min(vecs[edge[0]-i][1], vecs[y-i][1]) - vecs[y-i][0]) / (vecs[y-i][1]-vecs[y-i][0]) > 0.5 or \
                        float( min(vecs[edge[0]-i][1], vecs[y-i][1]) - vecs[y-i][0]) / (vecs[edge[0]-i][1]-vecs[edge[0]-i][0]) > 0.5 ):
                        # vecs[y-i][1] > vecs[edge[0]-i][1] + 10:
                        edge = [y, cur, bit_cur]

                if len(edge)==0:
                    # if np.sum(dists, axis=1)[ pre ] == 0:
                    #     dists[ pre, size+1 ] = 1024
                    continue
                
                # Edge construction
                y, cur = edge[0], edge[1]
                dists[pre][cur] += 1
                if (pre, cur) not in detail:
                    detail[ (pre, cur) ] = [[x,y]]
                else:
                    detail[ (pre, cur)].append([x,y])
                # dists[0][cur] = 0
                # dists[pre][size+1] = 0
                print ("", "edge", pre, cur, vecs[x-i], vecs[y-i], sep="\t", file=fileLog)
                pass

            # Naive assemble
            vecs_lst_ = []
            vecs_src_ = []
            for idx, item in enumerate( vecs_src ):
                if idx==0:
                    vecs_lst_.append(vecs_lst[0])
                    vecs_src_.append(vecs_src[0])
                elif vecs[idx][1] > data[ vecs_src_[-1][1] ].taR:
                    vecs_lst_.append( vecs_lst[idx] )
                    vecs_src_.append([ vecs_src_[-1][1], vecs_src[idx][1] ])
            if len(vecs_lst_)>1:
                name_int, fasta = merge_faa(vecs_lst_, vecs_src_, data, item_lst, gene_faa, gene_lst)
                temp_rec.append( ( gene_lst[ data[i].tar ] + "_guided", fasta, species, vecs_lst ) )
            
            # merged_faa.append( ( gene_lst[ data[i].tar ] + "_guided", fasta, species ) )

            # print (">%s_%s\n%s" %
            #     (species, gene_lst[ data[i].tar ] + "_guided", fasta), 
            #     file=fileFaa
            # )
            pass
                
        i = j+1

    # Eliminate redundant assembled path for naive procedure
    # 1 2 3 4
    # 1 - 3 4
    add_rec = []
    for id_i, it_i in enumerate(temp_rec):
        vecs_i = it_i[3]
        flag_add = True
        for id_j, it_j in enumerate(add_rec):
            break
            vecs_j = it_j[3]
            dp = [ [ 0 for x in range(len(vecs_j)+1) ] for y in range(len(vecs_i)+1 ) ]
            for x in range(1, len(vecs_i)+1 ):
                for y in range(1, len(vecs_j)+1 ):
                    dp[x][y] = max( dp[x][y-1], dp[x-1][y] )
                    if vecs_i[x-1] == vecs_j[y-1]:
                        dp[x][y] = max( dp[x][y], dp[x-1][y-1]+1 )
            if dp[ len(vecs_i) ][ len(vecs_j) ] == len( vecs_i ):
                flag_add = False
                break
            elif dp[ len(vecs_i) ][ len(vecs_j) ] == len( vecs_j ):
                add_rec[id_j] = it_i
                flag_add = False
                break
        if flag_add:
            add_rec.append(it_i)

    for it in add_rec:
        # merged_faa.append( (it[0], it[1], it[2]) )
        for vec in it[3]:
            pass
            if gene_len[ item_lst[vec] ] > len(it[1]) * 0.5:
                continue
                pass
            exclude.add( item_lst[vec] )

    # if np.max(dists[1:size+1,1:size+1])>4:
    #     for i in range(1, size+1):
    #         for j in range(1, size+1):
    #             if dists[i][j]==1:
    #                 dists[i][j]=0
    #             pass
    #         pass
    #     pass
    
    # Network assemble
    # Build source and sink
    dists, circle = Eliminate_Circle(dists)
    degrees = dists>0
    in_degree = np.sum(degrees, axis=0)
    ou_degree = np.sum(degrees, axis=1)
    print (in_degree, file=fileLog)
    print (ou_degree, file=fileLog)
    print ("Circle", circle, file=fileLog)
    start_fragment = np.where(in_degree==0)[0][1:-1]
    end_gragment = np.where(ou_degree==0)[0][1:-1]
    dists[0, start_fragment] = 1024
    dists[end_gragment, size+1] = 1024
    for i in range(1, size+1):
        if dists[0,i]==1024 and dists[i, size+1]==1024:
            dists[0,i]=0
            dists[i, size+1] = 0
        pass

    # Print log
    for dist in dists:
        print (dist, file=fileLog)
    for k, v in detail.items():
        v.sort(key=lambda x: -( data[x[1]].taR - data[x[0]].taL - max(0, data[x[1]].taL-data[x[0]].taR ) ) )
        detail[k] = v
        print (k, v, file=fileLog)
    print ("", file=fileLog)
    flow, _, paths = Maxmium_Flow(size+1, dists)
    print (flow, "paths", len(paths), file=fileLog)
    for idx, path in enumerate(paths):
        # print (, file=fileLog)
        path_lst = path[1][1:-1]
        path_src = [-1]
        # if len(path_lst)==1:
        #     continue
        for order, fragment in enumerate(path_lst):
            if not order:
                continue
            path_src.append(detail[(path_lst[order-1], fragment)][0] )
        print (path[0], path[1], path_src, file=fileLog)
        print("XXXXXXX", file = fileLog)

        # continue
        name_int, fasta = merge_faa(path_lst, path_src, data, item_lst, gene_faa, gene_lst)
        merged_faa.append((str(group) + "_"+ str(idx), fasta, species) )
        
        for name, inter, q_index in name_int:
            #merged_coo.append([str(group)+"_"+str(idx), name, inter, species, q_index])
            merged_coo.setdefault(str(species)+"_"+str(group)+"_"+str(idx), []).append([name, inter])
            
    return exclude


def deal_alignments(
    filePath,
    gene_map,
    gene_lst,
    gene_len, 
    gene_spe,
    gene_rlt, 
    gene_faa,
    spe_tra,
    spe_tre,
    mcl_parm
):
    global fileLog
    global fileFaa
    global merged_faa
    global merged_coo
    

    # Get aligments files
    path_aligments = os.listdir( filePath + "/splitBlast" )
    fileLog = open(filePath + "/merge_log.txt", "w")
    fileFaa = [ None for _ in range(spe_tre.size+1) ]

    merged_faa = []
    merged_coo = dict()
    excludes = set()


    for idx, path_aligment in enumerate(path_aligments):
        
        # Reading tabular alignments
        file_alignment = open( filePath + "/splitBlast/"+path_aligment, "r")
        group = int(path_aligment[ path_aligment.find("_")+1: ])
        alignments = []
        print (file_alignment, mcl_parm[group][-1], sep="\t", file=fileLog)

        for line in file_alignment:
            alignments.append( Alignment(line.strip(), gene_map) )

            # Transcriptome filter
            if spe_tra[ gene_spe[alignments[-1].qry] ] == False:
                alignments.pop()
                continue
            # Isoform filter
            if alignments[-1].qry != gene_rlt[ alignments[-1].qry ]:
                alignments.pop()
                continue
                pass
            # Identity filter
            if alignments[-1].idt < 75 and \
                float(alignments[-1].mat)/( alignments[-1].mat + alignments[-1].mis ) < .85:
                # alignments.pop()
                # continue
                pass
            # Coverage filter chimera
            if float( alignments[-1].qrR - alignments[-1].qrL + 1 ) / gene_len[ alignments[-1].qry ] < .8:
                alignments.pop()
                continue
            # Coverage filter complete
            if float( alignments[-1].taR - alignments[-1].taL + 1 ) / gene_len[ alignments[-1].tar ] > .9:
                alignments.pop()
                continue
            # Length filter
            if gene_len[ alignments[-1].tar ] > mcl_parm[group][-1] * 2 \
                or gene_len[ alignments[-1].tar ] - mcl_parm[group][-1] > 150:
                alignments.pop()
                continue
                pass
        pass
        
        # Sort according to querySpecies, query, and bitScore
        alignments.sort(key=lambda x: ( gene_spe[x.qry], x.qry, -x.bit ) )

        # Deal species seperatly
        i = 0
        while i<len(alignments):
            data = []
            j = i-1
            while j+1<len(alignments) and gene_spe[ alignments[j+1].qry ] == gene_spe[ alignments[i].qry ]:
                j += 1
                data.append( alignments[j] )
            exclude = deal_species_aligments(
                group, 
                data,
                gene_map,
                gene_lst,
                gene_len,
                gene_spe,
                gene_faa,
                spe_tra,
                spe_tre,
                mcl_parm
            )
            excludes = excludes | exclude
            i = j+1

        # Close file
        file_alignment.close()
        print ("\n", file=fileLog)

    # Print Merged fasta
    for guide, fasta, species in merged_faa:
        fp = open(filePath + "/" + species + "_add.fa", "a")
        print (">%s_%s\n%s" % (species, guide, fasta), file=fp)

    # Print trinity fasta
    for i in range(1, len(gene_map)+1 ):
        # if i in excludes:
        #     continue
        species = gene_spe[i]
        if not spe_tra[ species ]:
            continue
        species =  spe_tre.lst[species]
        fp = open(filePath + "/" + species + "_add.fa", "a")
        print (">%s\n%s" % (gene_lst[i], gene_faa[i][1:]), file=fp)
        fp.close()

    # Print excluded fasta
    fp = open( filePath + "/exclude.txt", "w")
    for it in excludes:
        print("%d\t%s" % (it, gene_lst[it]), file=fp )
    fp.close()

    # Cose files
    fileLog.close()


    for fp in fileFaa:
        if not fp: continue
        fp.close()

    return merged_faa, merged_coo, excludes


if __name__ == "__main__":
    pass
