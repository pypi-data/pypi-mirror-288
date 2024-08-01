import sys
import numpy as np

def KeepTopReuslts(list_, keep, pos):
    """
        To keep top BLAST hits
    """
    out = []
    count = 0
    last = list_[0][pos]

    for i, it in enumerate(list_):
        if it[pos] != last:
            count = 0
        if keep and count>=keep:
            continue
        out.append(it)
        count += 1
        last = it[pos]
    return out


def FloodFill(matrix):
    """
        Flood Fill algrorithms to get 
        connected genes in merge procedure
    """

    def dfs(x, dep):
        cluster[x] = count
        order[x] = dep
        for i in range(len(matrix)):
            if cluster[i] < 0 and matrix[x][i]:
                dfs(i, dep+1)
    
    count = 0
    cluster = [-1 for _ in range( len(matrix) )]
    order   = [ 0 for _ in range( len(matrix) )]
    inDegree = [0 for _ in range( len(matrix) )]
    
    for i in range (len(matrix)):
        for j  in range(len(matrix)):
            if matrix[i][j]:
                inDegree[j] +=1
    
    for i in range(len(matrix)):
        if cluster[i]<0 and inDegree[i]==0:
            dfs(i, 0)
            count += 1
    return count, np.array(cluster), np.array(order)


def GetOverlap(lst, edge, faa, l, r, muscle):
    """
        Dynamic programmiing to find 
        Longest common sequence 
        and locate interval
    """
    faa_L , faa_R = faa[ lst[l] ], faa[ lst[r] ]

    # targetStartL, targetStartR, targetEndL, targetEndR
    queryStartL, queryEndL = edge[11], edge[12]
    queryStartR, queryEndR = edge[13], edge[14]
    targetStartL, targetEndL = edge[15], edge[16]
    targetStartR, targetEndR = edge[17], edge[18]

    dirta = targetEndL - targetStartR
    if dirta<=10:
        return False, [], []
    queryGapsL = edge[5] - (queryEndL - queryStartL + 1)
    queryGapsR = edge[8] - (queryEndR - queryStartR + 1)
    targetGapsL = edge[5] - (targetEndL - targetStartL + 1)
    targetGapsR = edge[8] - (targetEndR - targetStartR + 1)

    # Compute longest-common-substring
    # [ queryEndL - dirta +- gapsL,  querlEndL ]
    # [ queryStartR, queryStartR + dirta +- gapsR]    
    startL = max( queryEndL - dirta - targetGapsL, 1)
    endL = queryEndL
    startR = queryStartR
    endR = min( queryStartR + dirta + targetGapsR, queryEndR) 

    dp = np.zeros( (dirta+targetGapsL+2, dirta+targetGapsR+2), dtype=int)
    for i in range(startL, endL+1):
        for j in range(startR, endR+1):
            x = i-startL+1
            y = j-startR+1
            dp[x][y] = np.max( np.array([dp[x-1][y], dp[x][y-1] ]) ) 
            if faa_L[i]==faa_R[j] and dp[x-1][y-1]+1>dp[x][y]:
                dp[x][y] = dp[x-1][y-1] + 1

    
    file_ = open('deal_seg_.txt', mode='a')
    print (muscle[:-4], file=file_)
    print (edge, file=file_)
    print ('\ttranscript', lst[l], 'transcript', lst[r], 
            queryGapsL, queryGapsR, targetGapsL, targetGapsR, file=file_)
    print (faa_L[ startL : endL+1 ], file=file_)
    print (faa_R[ startR : endR+1 ], file=file_)
    print (np.max(dp),  np.where(dp==np.max(dp)), file=file_ )
    print (file=file_)
    file_.close()
                
    return True, dp, []


def CleanEdges(lst, edges, faa, muscle):
    """
        Judging whther to link two transcript segment
        if their aligment to guide gene overlaps
    """
    N = len(lst)
    getLen = lambda tmp: list( map(lambda x: len(x), tmp) )
    links = list( map(getLen, edges))
    links = np.array(links)

    confidence = [ [[] for i in range(N)] for j in range (N)]
    for i in range(N):
        for j in range(N):
            if not edges[i][j]:
                continue
            edge = edges[i][j][0]
            flag, overlap, intervals = GetOverlap(lst, edge, faa, i, j, muscle)
    return links, confidence



def MergeGene(lst, edges, faa, muscle):
    """
        Merge transcripts procedure
        this is a DFS procedure currently
    """
    
    def dfs(curr_gene, cur, log, cut):
        if ouDegree[curr_gene] == 0 and cut:
            flag_add = True
            for log_ in merged_genes:
                log_ = log_[1]
                if set(log).issubset(set(log_)):
                    flag_add = False
                    break
            if flag_add:    
                merged_genes.append([cur, log, cut])
            return

        for next_gene in range( len(lst) ):
            if not edges[curr_gene][next_gene]:
                continue
            if next_gene in log:
                continue    

            edge = edges[ curr_gene][ next_gene ][0]
            queryStartL, queryEndL = edge[11], edge[12]
            queryStartR, queryEndR = edge[13], edge[14]
            targetStartL, targetEndL = edge[15], edge[16]
            targetStartR, targetEndR = edge[17], edge[18]

            if len(log)==1:
                cur = faa[ lst[curr_gene] ][queryStartL: queryEndL+1 ]

            if targetEndR <= targetEndL:
                continue

            if targetEndL < targetStartR:
                pass
                dfs(next_gene, 
                    cur + faa[ lst[next_gene] ][queryStartR : queryEndR+1], 
                    log + [next_gene], 
                    cut+[False]
                )
            else:
                pass
                dfs(next_gene, 
                    cur + faa[ lst[next_gene] ][ queryStartR+(targetEndL-targetStartR)+1 : queryEndR+1], 
                    log + [next_gene], 
                    cut + [True]
                )
    
    merged_genes = []    
    inDegree = [0 for _ in range( len(lst) )]
    ouDegree = [0 for _ in range( len(lst) )]
    
    for i in range (len(lst)):
        for j  in range(len(lst)):
            if edges[i][j]:
                inDegree[j] += 1
                ouDegree[i] += 1
    
    if len(lst)>10:
        getLen = lambda tmp: list( map(lambda x: len(x), tmp) )
        dists = list( map(getLen, edges))
        for dist in dists:
            pass
            #print (dist)
        
    for i in range( len(lst) ):
        if inDegree[i]:
            continue
        dfs(i, '', [i], [])
    return merged_genes
