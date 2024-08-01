from __future__ import print_function
import sys

class Tree:

    def __init__(self, size, item_map, item_lst, item_tra):
        self.size = size
        self.map = item_map
        self.lst = item_lst
        self.tra = item_tra
        self.sons = [ [] for _ in range(size * 2) ]
        self.father = [ 0 for _ in range(size * 2) ]
        self.weight = [ 1 for _ in range(size * 2) ]
        self.genome = [ 1 for _ in range(size * 2) ]
        for i in range(1, self.size+1):
            self.genome[i] = int(not item_tra[i])
    
    def load_nwk(self, S):
        N = self.size
        stack = []
        i=0
        while i<len(S):
            if S[i]=='(':
                stack.append('(')
            elif S[i]==')':
                leafs=[]
                while True:
                    last=stack.pop()
                    if last=='(':
                        break
                    else:
                        leafs.append(last)
                N += 1
                self.weight[N] -= 1
                self.genome[N] -= 1
                stack.append(N)
                for leaf in leafs:
                    self.sons[N].append(leaf)
                    self.father[leaf] = N
                    self.weight[N] += self.weight[leaf]
                    self.genome[N] += self.genome[leaf]
            elif S[i]==',':
                pass
            elif S[i]==';':
                break
            else:
                name=''
                while S[i]!='(' and S[i]!=')' and S[i]!=',':
                    name += S[i]
                    i += 1
                i-=1
                if name in self.map:
                    stack.append(self.map[name])
                else:
                    print (name,'not in map.')
            i+=1
        # print (self.size)
        # for i in range(1, self.size+1):
        #     print ("%s\t%d\t%d" % (item_lst[i], i, self.father[i]), file=sys.stderr)
        # for i in range(self.size+1, self.size*2):
        #     print ("%s\t%d\t%d" % ("None", i, self.father[i]), file=sys.stderr)


    def lca(self, lst):
        if len(lst)==1: return lst[0]
        node=lst[0]
        arr=[]
        while node: 
            arr.append(node)
            node = self.father[node]
        dep=0
        for i in range(1, len(lst)):
            node=lst[i]
            temp=[]
            while node:
                temp.append(node)
                node = self.father[node]
            l = len(arr)-1
            r = len(temp)-1
            while arr[l]==temp[r]:
                l -= 1
                r -= 1
            dep=max(dep, l+1)
            #print arr, temp, dep
        return arr[dep]


    def dfs(self, cur):
        nodes = []
        if (cur<=self.size):
            if not self.tra[cur]: nodes.append(cur)
        else:
            # print ("\t%d %d" %(self.sons[cur][0], self.sons[cur][1]) )
            nodes.extend( self.dfs(self.sons[cur][0]) )
            nodes.extend( self.dfs(self.sons[cur][1]) )
        return nodes


    def find_guide_num(self, limit):
        self.guide = [ set() for _ in range(self.size+1) ]
        for i in range(1, self.size+1):
            if not self.tra[i]: continue
            cur = i
            while True:
                father = self.father[cur]
                if not father: 
                    break
                cur = father
                if self.genome[cur]>=limit:
                    break
            # print ("Node [%d] === Guide [%d] === %s" % (i, cur, self.dfs(cur)), file=sys.stderr )
            self.guide[i] = set( self.dfs(cur) )

        # for i, it in enumerate(self.guide):
        #     print (i, it, sep="\t")


    def find_guide_taxa(self):
        self.guide = [ set() for _ in range(self.size+1) ]
        for i in range(1, self.size+1):
            if not self.tra[i]: continue
            cur = i
            steps = 0
            while steps<6:
                father = self.father[cur]
                if not father: break
                cur = father
                steps += 1
            # print ("Node [%d] === Guide [%d] === %s" % (i, cur, self.dfs(cur)), file=sys.stderr )
            self.guide[i] = set( self.dfs(cur) )

        # for i, it in enumerate(self.guide):
        #     print (i, it, sep="\t")


    def _print_tree(self, fp, cur, dep, path):
        s = [" " for _ in range(6*dep-2)]
        path.append(cur)
        for i in range( len(path)-1 ):
            if ( i == len(path)-2 or path[i+1] == self.sons[ path[i] ][0]):
                s[6*i+3] = "|"
        if dep:
            print( "\t%s---%3d weight[%d] genome[%d]" % 
                ( "".join(s), cur, self.weight[cur], self.genome[cur]), 
                end="", file=fp
            )
        else:
            print ("", file=fp)
            print( "\t %3d weight[%d] genome[%d]" % 
                (cur, self.weight[cur], self.genome[cur]), 
                end="", file=fp
            )

        if cur <= self.size:
            print (" %s %s" % (self.lst[cur], self.tra[cur]), file=fp)
        else:
            print ("", file=fp)
            self._print_tree(fp, self.sons[cur][0], dep+1, path)
            self._print_tree(fp, self.sons[cur][1], dep+1, path)
        path.pop()


    def print_tree(self, fp):
        for i in range(1, self.size*2):
            if self.father[i]: continue
            path = []
            self._print_tree(fp, i, 0, path)
    


if __name__ == "__main__":
    pass
    item_map = { 
        "Alyrata" : 1,
        "Trancriptome_At" : 2,
        "Crubella" : 3,
        "Esalsugineum" : 4,
        "Cpapaya" :5,
        "Tcacao" : 6,
        "Mdomestica" : 7,
        "Gmax" : 8,
        "Vvinifera" : 9,
        "Mguttatus" : 10,
        "Dcarota" :11,
        "Zmays" : 12,
        "Osativa" : 13, 
        "Macuminata" : 14,
        "Atrichopoda" : 15 
    }
    item_lst = [
        "", 
        "Alyrata",
        "Trancriptome_At",
        "Crubella",
        "Esalsugineum",
        "Cpapaya",
        "Tcacao",
        "Mdomestica",
        "Gmax",
        "Vvinifera",
        "Mguttatus",
        "Dcarota",
        "Zmays",
        "Osativa",
        "Macuminata",
        "Atrichopoda"
    ]
    tree = Tree(15, item_map, item_lst)
    tree.load_nwk('((((((((((Alyrata,Trancriptome_At),Crubella),Esalsugineum),Cpapaya),Tcacao),(Mdomestica,Gmax)),Vvinifera),(Mguttatus,Dcarota)),((Zmays,Osativa),Macuminata)),Atrichopoda);')
    tree.print_tree(sys.stderr)
    print ( tree.lca([8,6]) )
    # z=read_nwk('((((((10090,10116),(9598,9606)),9615),13616),9031),(99883,7955));')
    # print (lca(z, [1,9]))
    # print (len(x), len(y), len(z))
