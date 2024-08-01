from __future__ import print_function
import os
import sys
import json
import numpy as np


def Maxmium_Flow(N, graph):

    # Find augment flow by BFS
    def bfs(N, graph, flows):
        
        # Initialize variables
        queue = [None, 0]
        links = [-1 for _ in range(N+1)]
        flow = [ 0 for _ in range(N+1)]
        flow[0] = 1024
        left, right = 0, 1

        # BFS procedure
        while left < right:
            left += 1
            cur = queue[left]
            # Expansion logic of BFS 
            for i in range(0, N+1):
                
                # Check flow status
                if flows[cur][i] < graph[cur][i] and flow[i]==0:    

                    # Push vertex into queue               
                    queue.append(i)
                    links[i] = cur
                    flow[i] = min( 
                        flow[cur], 
                        graph[cur][i]-flows[cur][i]
                    )
                    flow[i] = int(flow[i])
                    right += 1
                
                pass

        # Augment flow not found
        if flow[N] == 0:
            return 0
        else:
        # Augment flow found
            cur = N

            # Intercept path of augment flow
            while cur!=0:
                # print (" %d" % cur, end="")
                pre = links[cur]

                # Update flow condition
                flows[pre][cur] += flow[N]
                flows[cur][pre] -= flow[N]
                cur = pre
            # print (" -> %d" % flow[N])
            return flow[N]

    # Find answer
    def dfs(N, flows, cur, flow):
        if cur==N:
            return flow, [cur]
        for i in range(0, N+1):
            if flows[cur][i]>0:
                flow_, path_ = dfs(N, flows, i, min(flow, flows[cur][i]) )
                if flow_>0:
                    flows[cur][i] -= flow_
                    path = [cur]
                    path.extend(path_)
                    return flow_, path
            pass

        return 0, []


    # Count maximum flow
    total_flow = 0
    flows = np.zeros_like(graph, dtype=int)

    # Try to find augment flow
    while True:
        flow = bfs(N, graph, flows)
        total_flow += flow
        if flow ==0:
            break
    
    # Print flows
    cur_flow = 0
    flows_ = flows
    paths = []
    while cur_flow < total_flow:
        flow, path = dfs(N, flows_, 0, 1024)
        cur_flow += flow
        paths.append([flow, path])
    
    # Return maximum flow
    return total_flow, flows, paths



def toplogical(dists):
    graph = np.array(dists>0,dtype=int)
    in_degree = np.sum(graph, axis=0)
    exclude = [False for _ in range(dists.shape[0])]

    while np.sum(graph)>0:
        node = -1
        for i in range(dists.shape[0]):
            if in_degree[i]==0 and not exclude[i]:
                node = i
                in_degree -= graph[node]
                graph[node] = 0
                exclude[node] = True

                # print (graph)
                # print (in_degree)
                break
        if node<0:
            return False
            
    return True



def Eliminate_Circle(dists):
    N = dists.shape[0]-2
    graph = np.zeros_like(dists)
    edges = []
    for i in range(1,N+1):
        for j in range(1, N+1):
            if dists[i][j]>0:
                edges.append([ i, j, dists[i][j] ])
    edges.sort(key=lambda x: -x[2])

    if len(edges)==0:
        return dists, False
    if edges[0][2]<=5 or toplogical(dists):
        return dists, False
    else:
        for x, y, z in edges:
            graph[x][y] += z
            if not toplogical(graph):
                graph[x][y] -= z
        return graph, True
    


if __name__ == "__main__":

    graph = np.zeros( (6,6), dtype=int )
    graph[1,2] = 40
    graph[1,4] = 20
    graph[2,3] = 30
    graph[2,4] = 20
    graph[3,4] = 10
    graph[4,3] = 10
    valid = graph

    print (graph, "\n", sep="")
    graph = (Eliminate_Circle(graph))
    print (graph)
    
    degrees = graph>0
    in_degree = np.sum(degrees, axis=0)
    ou_degree = np.sum(degrees, axis=1)
    # print ("In", in_degree, np.where(in_degree==0)[0][1:-1])
    # print ("Ou", ou_degree, np.where(ou_degree==0)[0][1:-1])

    graph[0, np.where(in_degree==0)[0][1:-1] ] = 1024
    graph[np.where(ou_degree==0)[0][1:-1],5 ] = 1024
    # graph [4,5] = 1024
    # print (graph)
    
    N = 5

    flow, flows, paths = Maxmium_Flow(N, graph)
    print (flow)
    for path in paths:
        print (path)
    
    
    # print (flows)