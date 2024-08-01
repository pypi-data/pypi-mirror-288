from __future__ import print_function
import os
import sys
from .load_data import *
from .alignment import *
#from .options import GetArgs
from multiprocessing import Pool
import subprocess

N = 0
item_map = {}
item_faa = [ None ]
cluster_genes = [ None ]
#args = GetArgs(sys.argv[1:])

def muscle_isosvm(path, threads, thread, MSA):
    
    global item_map
    global item_faa
    global cluster_genes

    # Print log
    # print ("thread[%d]" % (thread), 
    #     file=sys.stderr
    # )
    
    # MUSCLE
    for i in range( 1, len(cluster_genes) ):

        if i % threads != thread: continue

        fp = open(path + str(thread) + "/cluster_" + str(i) + ".txt", "w")
        for it in cluster_genes[i]:
            print (">%s\n%s" % (item_faa[it][0], item_faa[it][1].replace("*", "")), file=fp)
        fp.close()
        
        if MSA == "mafft":
            os.system(
                str(MSA) + " --auto --quiet " + path + str(thread) + "/cluster_" + str(i) + ".txt" \
                + " > " + path + str(thread) + "/cluster_" + str(i) + ".fasta" \
            )
        elif MSA == "muscle":
            os.system(
                str(MSA) + " -in " + path + str(thread) + "/cluster_" + str(i) + ".txt" \
                + " -out " + path + str(thread) + "/cluster_" + str(i) + ".fasta" + " -quiet"\
            )

    # isoSVM
    cur_path = os.getcwd()
    print("thread[%d] isoSVM %s " % (thread, "../" + path + str(thread)))
    os.system("isosvm_wrapper.pl -dir " + cur_path + "/" + path + str(thread) )

    pass


def dfs(cluster_genes, gene_clusters, edges, cur, ancestor):

    cluster_genes[-1].append(cur)
    gene_clusters[cur] = ancestor

    for node in edges[cur]:
        if gene_clusters[node]: continue
        dfs(cluster_genes, gene_clusters, edges, node, ancestor)
    pass


def flood_fill(filePath, faa, threads):

    global N
    global item_map
    global item_faa
    global cluster_genes
    N = 0
    item_map = {}
    item_faa = [ None ]
    cluster_genes = [ None ]

    # Make temp dir
    try:
        os.system("rm -rf " + filePath)
        os.system("mkdir " + filePath)
    except Exception as e:
        pass

    # Load fasta
    item_faa = faa
    fileFaa = open(filePath + "/fasta.txt", "w")
    for idx, it in enumerate(faa):
        if not it: continue
        item_map[ it[0] ] = idx
        print (">%s\n%s" % (it[0], it[1]), file=fileFaa)
    fileFaa.close()
    N = len(item_map)

    # return 

    # DIAMOND alignment
    os.system("diamond makedb " \
        + "--in " + filePath+ "/fasta.txt " \
        + "--db " + filePath+ "/db_fasta " \
        + "--quiet"
    )
    os.system( "diamond blastp " \
        + "--query " + filePath + "/fasta.txt " \
        + "--db " + filePath + "/db_fasta " \
        + "--out " + filePath + "/align_fasta.txt "\
        + "--masking 0 --evalue 1e-5 --quiet" 
    )

    # Get clustering similar to cd-hit
    fileAli = open(filePath + "/align_fasta.txt", "r")
    degree_in = [ 0 for _ in range(N+1) ]
    edges = [ [] for _ in range(N+1) ]
    for line in fileAli:
        line = Alignment( line.strip(), item_map )
        if line.qry == line.tar: continue
        lenQry = len( faa[line.qry][1] )
        lenTar = len( faa[line.tar][1] )
        # Build an edge line.tar -> line.qry
        if ( (lenTar>lenQry or lenTar==lenQry and line.tar<line.qry ) \
            and line.idt>95 and float(line.qrR-line.qrL+1)/lenQry>0.90
        ):
            # if lenTar-lenQry > 50 and line.idt<99:
            #     continue
            degree_in[ line.qry ] += 1
            edges[ line.tar ].append( line.qry )
    fileAli.close()

    # Flood fill algorithm
    fileCluster = open(filePath + "/clusters_cdhit.txt", "w")
    fileOut = open(filePath + "/flood-fill.txt", "w")
    gene_clusters = [ 0 for _ in range(N+1) ]
    for i in range(1, N+1):
        if degree_in[i]: continue
        cluster_genes.append( [] )
        dfs(cluster_genes, gene_clusters, edges, i, i)
        for it in cluster_genes[-1]:
            print (
                "%d-[%s]:%d\t" % 
                (it, item_faa[it][0], len(faa[it][1]) ), 
                end="", 
                file=fileCluster 
            )
        print ("", file=fileCluster)
        print (">%s\n%s" % (item_faa[i][0], faa[i][1]), file=fileOut)
    fileCluster.close()
    fileOut.close()

    # Pring log info to stderr
    clusters = len(cluster_genes)-1
    print ("%d clusters" % clusters , file=sys.stderr)
    
    
def run_isosvm(filePath, faa, threads,MSA):

    global N
    global item_map
    global item_faa
    global cluster_genes
    N = 0
    item_map = {}
    item_faa = [ None ]
    cluster_genes = [ None ]

    # Make temp dir
    # try:
    #     os.system("rm -rf " + filePath)
    #     os.system("mkdir " + filePath)
    # except Exception as e:
    #     pass

    # Load fasta
    item_faa = faa
    fileFaa = open(filePath + "/fasta.txt", "w")
    for idx, it in enumerate(faa):
        if not it: continue
        item_map[ it[0] ] = idx
        print (">%s\n%s" % (it[0], it[1]), file=fileFaa)
    fileFaa.close()
    N = len(item_map)

    # return 

    # DIAMOND alignment
    os.system("diamond makedb " \
        + "--in " + filePath+ "/fasta.txt " \
        + "--db " + filePath+ "/db_fasta " \
        + "--quiet" 
    )
    os.system( "diamond blastp " \
        + "--query " + filePath + "/fasta.txt " \
        + "--db " + filePath + "/db_fasta " \
        + "--out " + filePath + "/align_fasta.txt "\
        + "--masking 0 --evalue 1e-5 --quiet"
    )

    # Get clustering similar to cd-hit
    fileAli = open(filePath + "/align_fasta.txt", "r")
    degree_in = [ 0 for _ in range(N+1) ]
    edges = [ [] for _ in range(N+1) ]
    for line in fileAli:
        line = Alignment( line.strip(), item_map )
        if line.qry == line.tar: continue
        lenQry = len( faa[line.qry][1] )
        lenTar = len( faa[line.tar][1] )
        # Build an edge line.tar -> line.qry
        if ( (lenTar>lenQry or lenTar==lenQry and line.tar<line.qry ) \
            and line.idt>90 and float(line.qrR-line.qrL+1)/lenQry>0.90
        ):
            # if lenTar - lenQry > 50 and line.idt < 99.5:
            #     continue
            degree_in[ line.qry ] += 1
            edges[ line.tar ].append( line.qry )
    fileAli.close()

    # Flood fill algorithm
    fileCluster = open(filePath + "/clusters_isosvm.txt", "w")
    gene_clusters = [ 0 for _ in range(N+1) ]
    for i in range(1, N+1):
        if degree_in[i]: continue
        cluster_genes.append( [] )
        dfs(cluster_genes, gene_clusters, edges, i, i)
        if len(cluster_genes[-1])==1:
            cluster_genes.pop()
            continue
        for it in cluster_genes[-1]:
            print (
                "%d-[%s]:%d\t" % 
                (it, item_faa[it][0], len(faa[it][1]) ), 
                end="", 
                file=fileCluster 
            )
        print ("", file=fileCluster)
    fileCluster.close()
    
    # Pring log info to stderr
    clusters = len(cluster_genes)-1
    part = max(1, clusters / threads )
    print ("%d clusters" % clusters , file=sys.stderr)
    
    # Make fasta dir for muscle and isoSVM
    try:
        os.system("rm -rf " + filePath + "/part_*" )
        for i in range(threads):
            os.system("mkdir " + filePath + "/part_" + str(i) )
    except Exception as e:
        pass
    
    # Multi threads muscle and isoSVM
    pools = Pool(threads)
    path = filePath + "/part_"
    # print (path, file=sys.stderr)
    print("mafft")
    for i in range(threads):
        l = i*part
        r = i*part + part
        if i==0:
            l = 1
        if i==threads-1:
            r = clusters+1
        pools.apply_async( muscle_isosvm, args=(path, threads, i,MSA) )
        pass
    pools.close()
    pools.join()

    # Cat log file
    os.system("cat " + path + "*/*log > " + filePath + "/isoform.log")
  

def get_isosvm(filePath, faa):

    global N
    global item_map
    global item_faa

    fileIsosvm = open(filePath + "/isoform.log", "r")
    fileIsoform = open(filePath + "/isoform.txt", "w")
    fileClean = open(filePath + "/clean_fasta.txt", "w")
    fileLog = open(filePath + "/log.txt", "w")

    edges = [ [] for _ in range(N+1) ]
    degree = [ 0 for _ in range(N+1) ]

    for line in fileIsosvm:
        line = line.strip("\n").split(" ")
        # print (line)

        if line[0] == "Sequence": 
            x = item_map[ line[2][2:len(line[2])-2] ]
            if line[3] == "unknown/ignored":
                label = "unknown/ignored"
            elif line[5] == "paralog":
                label = "paralog"
            elif line[5] == "splice-variant":
                label = "splice-variant"
            else:
                print ("wrong", line)
        elif line[0] == "done" and len(line)==1:
            pass 
            # for i in degree: 
            #     print (i, degree[i], gene_len[i], file=file_iso)
            #     pass
            # print ("", file=file_iso)
            # degree = {}
        elif len(line)<4:
            continue
        elif len(line[3])>0 and line[3][0] == "#":
            y = item_map[ line[4][2:len(line[4])-5] ]
            if label == "unknown/ignored":
                if line[14] == "1": 
                    label="same"
                elif line[14] == "0": 
                    label="zero"
                else: 
                    print ("wrong", line)
                    break

            # Build an edge x -> y
            x_ = x
            y_ = y 
            if len(faa[x_][1]) < len(faa[y_][1]) \
                or len(faa[x_][1]) == len(faa[y_][1]) and x>y:
                x_, y_ = y_, x_
            if (label=="splice-variant" or label=="same"):
                degree[y_]+=1
                edges[x_].append(y_)
                print ("%d[%s]-%d %d[%s]-%d" % 
                    (x_, faa[x_][0], len(faa[x_][1]), 
                    y_, faa[y][0], len(faa[y_][1])), 
                    file=fileLog
                )
            else:
                pass 
        pass
    fileIsosvm.close()

    # Flood fill algorithm
    isoform_genes = [None]
    genes_isoform = [ 0 for i in range(N+1) ]
    for i in range(1, N+1):
        if degree[i]: continue
        isoform_genes.append( [] )
        dfs(isoform_genes, genes_isoform, edges, i, i)
        # if len(isoform_genes[-1])==1: continue
        for it in isoform_genes[-1][1:]:
            # print ("%d-[%s]:%d\t" % 
            #     (it, item_faa[it][0], len(faa[it][1]) ), end="", 
            #     file=fileIsoform
            # )
            print ("%s\t%s" % 
                (item_faa[it][0], item_faa[ isoform_genes[-1][0] ][0]), 
                file=fileIsoform
            )
        print ("", file=fileIsoform)
        print (">%s\n%s" % 
            (item_faa[ isoform_genes[-1][0] ][0], item_faa[ isoform_genes[-1][0] ][1] ),
            file=fileClean
        )
        pass

    fileIsoform.close()
    fileClean.close()
    fileLog.close()

    pass
    return isoform_genes


def deal_blast(gene, arr):
    
    global ref

    out = []
    for k, v in arr.items():
        v = np.array(v)
        out.append([k, np.sum(v), np.average(v)])
        if len(v)>1 or True:
            pass
            #print ('paralog', k, v)
    out.sort(key=lambda x: -x[2])
    ans = []
    for i, (k, sum_, ave_,) in enumerate(out):
        if (i==5 or ave_<out[0][2]*0.9) and (gene<=ref and k!=gene_grp[gene]):
            # return out[:i]
            continue
        ans.append([ k, sum_, ave_ ])
    return ans



def get_isosvm_OG(filePath, faa, gene_map_, gene_lst_, gene_ass_, gene_grp, merged_coo):

    global N
    global item_map
    global item_faa

    gene_map = gene_map_
    gene_lst = gene_lst_
    gene_ass = gene_ass_

    """
    # Get alignment
    fileAdd = open(filePath + "/add.txt", "w")
    for gene, sequence in item_faa[1:]:
        if gene.find("guided") == -1:
            continue
        gene_map[gene] = len(gene_lst)
        gene_lst.append(gene)
        print (">%s\n%s" % (gene,sequence), file=fileAdd)
    fileAdd.close()
    print ("Renewd gene_map %d" % len(gene_map), file=sys.stderr)

    # Get addtional fa to ref alignment 
    fileRef = open(filePath + "/ref.txt", "w")
    for gene, sequence in database[1:]:
        print (">%s\n%s" % (gene, sequence), file=fileRef)
    fileRef.close()

    os.system("diamond makedb " \
        + "--in " + filePath+ "/ref.txt "\
        + "--db " + filePath+ "/db_ref")
    os.system( "diamond blastp " \
        + "--query " + filePath + "/add.txt " \
        + "--db " + filePath + "/db_ref " \
        + "--out " + filePath + "/align_ref.txt "\
        + "--masking 0 --evalue 1e-5" 
    )

    # Renew gene_ass
    fileAli = open(filePath + "/align_ref.txt", "r")
    temp = {}
    last_gene = None
    for x, line in enumerate(fileAli):
        line = line.strip().split()
        gene0, gene1 = item_map[line[0]], gene_map[line[1]]
        group1 = gene_grp[gene1]
        
        if gene0==None or gene1==None:
            print ("line", x, "BLAST is illeagal")
            continue

        if last_gene!=None and gene0!=last_gene:
            gene_ass[last_gene] = deal_blast(last_gene, temp)
            temp = {}

        if group1 in temp:
            temp[group1].append(float(line[-1]))
        else:
            temp[group1] = [float(line[-1])]
        last_gene = gene0
    gene_ass[last_gene] = deal_blast(last_gene, temp)
    fileAli.close()
    """

    # Print gene assign
    fileNewAss = open(filePath + "/new_ass.txt", "w")
    for k, v in gene_ass.items():
        print (k, item_faa[k][0], file=fileNewAss)
        for it in v:
            print ("\t%s" % str(it), file=fileNewAss )
    fileNewAss.close()

    # Get isoform
    fileIsosvm = open(filePath + "/isoform.log", "r")
    fileIsoform = open(filePath + "/isoform.txt", "w")
    fileClean = open(filePath + "/clean_fasta.txt", "w")
    fileLog = open(filePath + "/log.txt", "w")
    fileCoo = open(filePath + "/assemble_coo.txt", "w")

    edges = [ [] for _ in range(N+1) ]
    degree = [ 0 for _ in range(N+1) ]

    for line in fileIsosvm:
        line = line.strip("\n").split(" ")
        # print (line)

        if line[0] == "Sequence": 
            x = item_map[ line[2][2:len(line[2])-2] ]
            if line[3] == "unknown/ignored":
                label = "unknown/ignored"
            elif line[5] == "paralog":
                label = "paralog"
            elif line[5] == "splice-variant":
                label = "splice-variant"
            else:
                print ("wrong", line)
        elif line[0] == "done" and len(line)==1:
            pass 
            # for i in degree: 
            #     print (i, degree[i], gene_len[i], file=file_iso)
            #     pass
            # print ("", file=file_iso)
            # degree = {}
        elif len(line)<4:
            continue
        elif len(line[3])>0 and line[3][0] == "#":
            y = item_map[ line[4][2:len(line[4])-5] ]
            if label == "unknown/ignored":
                if line[14] == "1": 
                    label="same"
                elif line[14] == "0": 
                    label="zero"
                else: 
                    print ("wrong", line)
                    break
            if label == "splice-variant":
                pass
                # if float( line[14] )< 0.95:
                #     continue

            # Build an edge x -> y
            x_ = x
            y_ = y
            
            compare = 0
            if item_faa[x_][0] in gene_map and item_faa[y_][0] in gene_map:
                group_x = set()
                group_y = set()
                score_x = {}
                score_y = {}
                for it in gene_ass.get(x_, []):
                    group_x.add( it[0] )
                    score_x[ it[0] ] = it[2]
                for it in gene_ass.get(y_, []):
                    group_y.add( it[0] )
                    score_y[ it[0] ] = it[2]
                intersection = group_x & group_y
                for group in intersection:
                    if abs( score_x[group] - score_y[group] ) < 0.2:
                        continue
                    if score_x[group] > score_y[group]:
                        compare += 1
                    else:
                        compare -= 1
                if compare < 0:
                    x_, y_ = y_, x_
                # print ("%d[%s] [%s] === %d[%s] [%s]" % 
                #     (x, item_faa[x][0], str(score_x),
                #      y, item_faa[y][0], str(score_y) )
                # )
            
            if compare==0:
                if len(faa[x_][1]) < len(faa[y_][1]) \
                    or len(faa[x_][1]) == len(faa[y_][1]) and x>y:
                    x_, y_ = y_, x_
            
            # if abs( len(faa[x_][1]) - len(faa[y_][1]) ) > 100:
            #     continue

            if (label=="splice-variant" or label=="same"):
                degree[y_]+=1
                edges[x_].append(y_)
                print ("[%d:%s] %d\n\t%s\n[%d:%s] %d\n\t%s\n" % 
                    (x_, faa[x_][0], len(faa[x_][1]), str(gene_ass.get(x_, "NA")),
                    y_, faa[y][0], len(faa[y_][1]), str(gene_ass.get(y_, "NA")) ),
                    file=fileLog
                )
            else:
                pass 
        pass
    fileIsosvm.close()

    # Flood fill algorithm
    isoform_genes = [None]
    genes_isoform = [ 0 for i in range(N+1) ]
    for i in range(1, N+1):
        if degree[i]: continue
        isoform_genes.append( [] )
        dfs(isoform_genes, genes_isoform, edges, i, i)
        # if len(isoform_genes[-1])==1: continue
        for it in isoform_genes[-1][1:]:
            print ("%s\t%s" % 
                (item_faa[it][0], item_faa[ isoform_genes[-1][0] ][0]), 
                file=fileIsoform
            )
        # print ("", file=fileIsoform)
        # print clean fasta
        print (">%s\n%s" % 
            (item_faa[ isoform_genes[-1][0] ][0], item_faa[ isoform_genes[-1][0] ][1] ),
            file=fileClean
        )
        #print new gene assemble coordinate
        if item_faa[ isoform_genes[-1][0]] [0] in merged_coo:
            fileCoo.write(str(item_faa[ isoform_genes[-1][0]] [0])+"\t")
            for i in merged_coo[item_faa[ isoform_genes[-1][0]] [0]]:
                fileCoo.write(str(i))
                fileCoo.write("\t")
            fileCoo.write("\n")
        else:
            fileCoo.write(str(item_faa[isoform_genes[-1][0]] [0]))
            fileCoo.write("\n")
                       
        
    fileIsoform.close()
    fileClean.close()
    fileLog.close()
    fileCoo.close()

    # exact the new cds sequence according to the assemble coordinate
   # print(os.getcwd())
    #print(args.filePep)
    #print(args.fileCds)
    #print(filePath)
    #print("perl SingleForTransmcl.pl " + filePath + "/assemble_coo.txt" + " " + "new_assembled" + " " + args.fileThr + " " + args.fileCds + " " +args.filePep)
    #p = subprocess.run("perl SingleForTransmcl.pl " + filePath + "/assemble_coo.txt" + " " + "new_assembled" + " " + args.fileThr + " " + args.fileCds + " " +args.filePep, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pass
    return isoform_genes



if __name__ == "__main__":
    if len(sys.argv)<7:
        print ("python isosvm.py fasta_file gene_map gene_group output_prefix threads")
        exit()
    
    fileInput = open(sys.argv[1], "r")
    # fileDB = open(sys.argv[2], "r")
    fileMap = open(sys.argv[2], "r")
    fileAss = open(sys.argv[3], "r")
    fileGrp = open(sys.argv[4], "r")
    threads = int(sys.argv[6])

    # load fasta
    for line in fileInput:
        line = line.strip().split()
        if line[0][0] == ">":
            item_faa.append([ line[0][1:], "" ])
        else:
            item_faa[-1][1] += line[0]
    fileInput.close()

    # load DB
    # db = [None]
    # for line in fileDB:
    #     line = line.strip().split()
    #     if line[0][0] == ">":
    #         db.append([ line[0][1:], "" ])
    #     else:
    #         db[-1][1] += line[0]
    # fileDB.close()

    # load gene_map
    ref, M, gene_lst, gene_map = load_info(fileMap)

    # load gene_grp
    gene_grp = {}
    for line in fileGrp:
        line = line.strip().split()
        gene = gene_map.get(line[0], None)
        if not gene:
            continue
        gene_grp[gene] = int( line[1] )
    print ("%d fasta read" % len(item_faa), file=sys.stderr)

    flood_fill(sys.argv[5], item_faa, threads)

    run_isosvm(sys.argv[5], item_faa, threads)
    # get_isosvm(sys.argv[6], item_faa)
    # exit()

    # load gene_ass
    gene = None
    gene_ass = {}
    for idx, line in enumerate(fileAss):
        line = line.rstrip().split("\t")

        if  len(line)==1:
            continue
        if line[0]:
            gene = item_map.get( line[1], None)
        else:
            if not gene:
                continue
            group, sum_, ave_ = int(line[1]), float(line[2]), float(line[3])
            if gene not in gene_ass:
                gene_ass[gene] = [ [group, sum_, ave_] ]
            else:
                gene_ass[gene].append([ group, sum_, ave_ ])
    print ("original gene_ass %d" % len(gene_ass), file=sys.stderr)
                
    get_isosvm_OG(
        sys.argv[5],
        item_faa,
        gene_map,
        gene_lst,
        gene_ass,
        gene_grp
    )
    pass
