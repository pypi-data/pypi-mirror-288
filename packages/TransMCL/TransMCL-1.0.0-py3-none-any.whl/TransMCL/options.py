from __future__ import print_function
import sys
import getopt

class GetArgs:

    def __init__(self, argv):

        # Initialize variables
        self.fileAbc = None
        self.fileAli = None
        self.fileFaa = None
        self.filePep = None
        self.fileGrp = None
        self.fileIfo = None
        self.fileLen = None
        self.fileOut = None
        self.fileIso = None
        self.fileSpe = None
        self.fileTre = None
        self.fileThr = None

        try:
            opts, args=getopt.getopt(argv, "h", [
                "help", 
                "abc=",
                "alignment=",
                "pep=",
                "group=",
                "info=", 
                "length=", 
                "out=",
                "isoform=",
                "species=",                        
                "transcriptome=",
                "tree=",
                "threads=",
                "MSA=",
                ]
            )
        except getopt.GetoptError as err:
            print (err)
            sys.exit(1)

        try:
            for arg, val in opts:
                print(arg, val)
                if arg in ("--help", "-h") or arg ==None:
                    print ("Usage")
                elif arg in ("--abc"):
                    self.fileAbc = open(val, "r")
                elif arg in ("--alignment"):
                    self.fileAli = open(val, "r")
                elif arg in ("--pep"):
                    self.fileFaa = open(val, "r")
                    self.filePep = val
                elif arg in ("--group"):
                    self.fileGrp = open(val, "r")
                elif arg in ("--info"):
                    self.fileIfo = open(val, "r")
                elif arg in ("--length"):
                    self.fileLen = open(val, "r")
                elif arg in ("--out"):
                    self.fileOut = val
                elif arg in ("--isoform"):
                    try:
                        self.fileIso = open(val, "r")
                    except Exception as e:
                        self.fileIso = None
                        print (e, file=sys.stderr)
                elif arg in ("--species"):
                    self.fileSpe = open(val, "r")
                elif arg in ("--transcriptome"):
                    self.fielTra = open(val, "r")
                elif arg in ("--tree"):
                    self.fileTre = open(val, "r")
                elif arg in ("--threads"):
                    self.fileThr = val
                
        except Exception as e:
            print (e)
            sys.exit(1)

