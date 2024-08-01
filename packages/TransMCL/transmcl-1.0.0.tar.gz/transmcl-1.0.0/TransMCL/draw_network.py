from __future__ import print_function
import sys
import json
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def dfs(matrix, cur, dep, stamp):

    stamp[cur] = dep
    for i in range( len(matrix)-1 ):
        if matrix[cur][i] < 0.1:
            continue
        if stamp[i] != 0:
            continue
        dfs(matrix, i, dep+1, stamp)
    
def draw(matrix, fp="example.png"):

    G=nx.DiGraph()
    dim = matrix.shape[0]
    row_sum = np.sum(matrix, 1)
    col_sum = np.sum(matrix, 0)
    print (row_sum)
    print (col_sum)

    for i in range(dim):
        G.add_node(i)
        if i==0 or i==dim-1:
            continue
        if row_sum[i] < 0.1:
            matrix[i][dim-1] = 1.
        if col_sum[i] < 0.1:
            matrix[0][i] = 1.
        
    dep = 1
    stamp = np.zeros(dim, dtype=int)
    dfs(matrix, 0, dep, stamp)
    stamp[dim-1] = np.max(stamp) + 1
    print ("stamp", stamp)

    count = np.zeros(dim)
    pos = np.zeros( (dim,2) )
    for i in range(dim):
        count[ stamp[i] ] += 1
        pos[i][0] = stamp[i]
        pos[i][1] = count[ stamp[i] ]
    print (pos)
    # print ( np.max(pos[:,1]) )
    pos[0][1] = int( np.max(pos[:,1])/2 ) + .5
    pos[dim-1][1] = int( np.max(pos[:,1])/2 ) + .5

    for i in range(dim):
        for j in range(dim):
            if matrix[i][j]==0:
                continue
            G.add_edge(i, j, weight=matrix[i][j])


    nx.draw(G, pos, with_labels=True)

    # elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >1.01]
    # esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=1.01]
    # pos=nx.spring_layout(G)
    # nx.draw_networkx_nodes(G,pos,node_size=700)
    # nx.draw_networkx_edges(G, pos,
    #     edgelist=elarge,
    #     width=6
    # )
    # nx.draw_networkx_edges(G, pos,
    #     edgelist=esmall,
    #     width=6, 
    #     alpha=0.5,
    #     edge_color='b',
    #     style='dashed'
    # )  
    # nx.draw_networkx_labels(G, pos, 
    #     font_size=10,
    #     font_family='sans-serif'
    # )
    # plt.axis("off")

    plt.savefig(fp) # save as png


if __name__ == "__main__":
    
    if len(sys.argv)<3:
        # print ("python assemble_status.py input_file output_file")
        # exit()
        pass
    matrix = np.array([
        [0,1,2],
        [0,0,3],
        [4,0,0],
    ])

    matrix = np.array([
        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 4., 0., 3., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 2., 0., 0., 0., 0.],
        [ 0.,  0.,  2.,  0.,  0., 16.,  0.,  4.,  0.,  0.,  0.],
        [0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 8., 0., 7., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 1., 0., 0., 3., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    ])

    matrix = np.array([
        [0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 4., 0., 0., 0., 0.],
        [0., 0., 0., 4., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 1., 2., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0.]
    ])

    draw(matrix)