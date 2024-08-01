#! /usr/local/bin/python3

from __future__ import print_function
import os
import sys
from .load_data import *
import getopt
from .species_gene import get_isoform, get_species_gene
from .isosvm import *
import subprocess
from .merge_gene import deal_alignments
from time import *

begin_time = time()

def Usage():
    print("""
    Usage: python3 -m TransMCL [option] [parameter]
    --abc       input mcl abc file
    --info      input mcl info file
    --alignment input all-to-all blast file
    --fasta     input transcriptome file(.pep)
    --group     input mcl group file
    --length    input gene length file
    --species   input gene species file
    --transcriptome input transcriptome list
    --tree      input tree file(.nwk)
    --MSA	input MSA tool (mafft/muscle; default:mafft)
    --threads   threads
    --out       output file name
    """)

if __name__ == "__main__":
    fileAbc, fileAli, fileFaa, fileGrp, fileIfo, fileLen, fileOut, fileIso, fileSpe, fileTra, fileTre, fileThr = [None]*12    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", 
            [
            "help",
            "abc=",
            "info=",
            "alignment=",
            "fasta=",
            "group=",
            "length=",
            "species=",
            "transcriptome=",
            "tree=",
            "MSA=",
            "threads=",
            "out="
            ]
        )
       
        if not len(opts):
            Usage()
            exit()
        fileMSA = "mafft"                 #defaut msa tool
        print("[msa tool]:".ljust(20), fileMSA)
        for arg, val in opts:
            if arg in ("--help", "-h"):
                Usage()
                sys.exit(1)
            elif arg in ("--abc"):
                fileAbc = open(val, "r")
                print("[abc file]:".ljust(20), val)
            elif arg in ("--alignment"):
                fileAli = open(val, "r")
                print("[alignment file]:".ljust(20), val)
            elif arg in ("--fasta"):
                fileFaa = open(val, "r")
                print("[fasta file]:".ljust(20), val)
            elif arg in ("--group"):
                fileGrp = open(val, "r")
                print("[group file]:".ljust(20), val)
            elif arg in ("--info"):
                fileIfo = open(val, "r")
                print("[info file]:".ljust(20), val)
            elif arg in ("--length"):
                fileLen = open(val, "r")
                print("[length file]:".ljust(20), val)
            elif arg in ("--out"):
                fileOut = val
                print("[output dir]:".ljust(20), val)
            elif arg in ("--isoform"):
                try:
                    fileIso = open(val, "r")
                except Exception as e:
                    fileIso = None
                    print (e, file=sys.stderr)
            elif arg in ("--species"):
                fileSpe = open(val, "r")
                print("[spe file]:".ljust(20), val)
            elif arg in ("--transcriptome"):
                fileTra = open(val, "r")
                print("[transcriptome file]:".ljust(20), val)
            elif arg in ("--tree"):
                fileTre = open(val, "r")
                print("[tree file]," .ljust(20), val)
            elif arg in ("--MSA"):
                fileMSA = val
                print("using MSA tools:".ljust(20), val)
            elif arg in ("--threads"):
                fileThr = val
                print("using threads:".ljust(20), val)
    
    except getopt.GetoptError as e:
        print (e)
        Usage()
        sys.exit(1)

    try:
        # os.system("rm -rf " + args.fileOut)
        os.system("mkdir " + fileOut)
        os.system("rm -rf " + fileOut + "/*_add.fa")
        os.system("mkdir " + fileOut + "/splitBlast")
        os.system("mkdir " + fileOut + "/isosvm_1st")
        os.system("mkdir " + fileOut + "/isosvm_2nd")
       
    except Exception as e:
        pass

    # Loading info file
    N, M, gene_lst, gene_map = load_info(fileIfo)

    # Loading fasta file
    gene_faa = load_faa(fileFaa, gene_map)

    # Loading length file
    gene_len = load_len(fileLen, gene_map)

    # Loading species file
    spe_lst, spe_map, gene_spe = load_spe(fileSpe, gene_map)

    # Loading transcriptome file
    spe_tra = load_tra(fileTra, spe_map)

    # Loading species tree
    spe_tre = load_tre(fileTre, spe_map, spe_lst, spe_tra,)

    # Loading OGs
    gene_grp, mcl_list, mcl_parm = load_mcl(
        fileGrp, fileOut, spe_tre, spe_tra, 
        gene_map, gene_spe, gene_len
    )

    # Loading abc
    gene_ass = load_abc(
        fileAbc, fileOut, 
        gene_map, gene_lst, 
        gene_grp, gene_spe, spe_tra
    )

    # Loading Aligments
    load_blast(
        fileAli, fileOut, 
        gene_map, gene_grp, gene_ass, gene_spe, 
        spe_tra, spe_tre
    )

    #os.system("ps aux|grep TransMCL|grep output_test1 > memory.txt")   
    print("step 1")
    # Loading isoSVM result
    if fileIso:
        gene_rlt = load_rlt(fileIso, int(fileThr))
    else:
        gene_rlt = get_isoform(
            fileOut + "/isosvm_1st",
            gene_map,
            gene_lst,
            gene_grp,
            gene_ass,
            gene_faa,
            gene_spe,
            [],
            set(),
            spe_map,
            spe_tra,
            int(fileThr),
            [],
            fileMSA
        )
    #os.system("ps aux|grep TransMCL|grep output_test1 >> memory.txt")
    # Merge Genes
    print("step 2")
    merged_faa, merged_coo, excludes= deal_alignments(
        fileOut, 
        gene_map, gene_lst,
        gene_len, gene_spe, 
        gene_rlt, gene_faa, 
        spe_tra, spe_tre,
        mcl_parm
    )
    #os.system("ps aux|grep TransMCL|grep output_test1>> memory.txt")
    # exit()
    print("step 3")
    get_isoform(
        fileOut + "/isosvm_2nd",
        gene_map,
        gene_lst,
        gene_grp,
        gene_ass,
        gene_faa,
        gene_spe,
        merged_faa,
        # excludes, 
        set(),
        spe_map,
        spe_tra,
        int(fileThr),
        merged_coo,
        fileMSA
    )
    #os.system("ps aux|grep TransMCL >> memory.txt")
    # Clean genes
    
    # calculate time
    end_time = time()
    print("total_time:%ss" %(end_time-begin_time))

    exit(0)

