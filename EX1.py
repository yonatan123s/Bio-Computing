# This program gets a number n and return all the connected sub-graphs of size n.

import numpy as np
import itertools

def create_graphs(n):
    #this function returns all the graphs of size n
    graphs = []
    for i in range(2**(n**2)):
        flag =0
        bin_string = bin(i)
        bin_string = bin_string[2:len(bin_string)]
        for k in range(n**2-len(bin_string)):
            bin_string = '0' + bin_string
        new_string = ''
        for k in range(n**2):
            if((k+1)%n == 0 and k!= 0):
                new_string += bin_string[k] + "; "
            else:
                new_string += bin_string[k] + " "
        new_string = new_string[0:len(new_string)-2]
        graph = np.matrix(new_string)
        for m in range(len(graph)):
            for l in range(len(graph)):
               if l==m and graph[l,m] ==1:
                   flag = 1
        if flag == 0:
            graphs.append(graph)
    return graphs

def undirecet_graph(graph_matrix):
    #this function gets a graph and returns the undirected graph with the same edges
    new_graph_matrix = np.zeros((len(graph_matrix), len(graph_matrix)))
    for i in range(len(graph_matrix)):
        for j in range(len(graph_matrix)):
            if graph_matrix[i,j] == 1 or graph_matrix[j,i] == 1:
                new_graph_matrix[i,j] = 1
                new_graph_matrix[j,i] = 1
    return new_graph_matrix

def check_con(graph_matrix):
    #this function checks if a graph is connected
    n = len(graph_matrix)
    mat = undirecet_graph(graph_matrix)
    visited_vertices = [0]*n
    visited_vertices[0] = 1
    vertices_stack = []
    vertices_stack.append(0)
    while len(vertices_stack) != 0:
        vertex = vertices_stack.pop()
        for i in range(n):
            if i != vertex and mat[vertex,i] == 1 and visited_vertices[i] == 0:
                vertices_stack.append(i)
                visited_vertices[i] = 1
    for k in range(n):
        if visited_vertices[k] == 0:
            return False
    return True


# Python function to print permutations of a given list
def permutation(lst):
    #this function returns all the permutation of a list
    #this code was taken from GeeksForGeeks
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []

    # If there is only one element in lst then, only
    # one permutation is possible
    if len(lst) == 1:
        return [lst]

    # Find the permutations for lst if there are
    # more than 1 characters

    l = []  # empty list that will store current permutation

    # Iterate the input(lst) and calculate the permutation
    for i in range(len(lst)):
        m = lst[i]

        # Extract lst[i] or m from the list.  remLst is
        # remaining list
        remLst = lst[:i] + lst[i + 1:]

        # Generating all permutations where m is first
        # element
        for p in permutation(remLst):
            l.append([m] + p)
    return l



def check_iso(mat1, mat2):
    #this function checks if two matrices represents isomorphic graphs
    per_list = [i for i in range(len(mat1))]
    permutations = permutation(per_list)
    iden_mat = np.identity(len(mat1))
    #the problem is the dimensions
    dime = (len(mat1), len(mat1))
    for i in permutations:
        per_mat = np.zeros(dime)
        for j in i:
            per_mat[j,i[j]] = 1
        inv_per = np.linalg.inv(per_mat)
        new_mat = np.matmul(inv_per, mat1)
        new_mat = np.matmul(new_mat,per_mat)
        if np.allclose(new_mat , mat2):
            return True
    return False


def print_graph(graph):
    #this function get a graph as string and outputs it in the
    #requested format
    graph_str = ""
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i,j] == 1:
                graph_str += str(i) + " " + str(j)+"\n"
    graph_str = graph_str[:-1]
    return graph_str

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

def create_sub_graph(graph, index_sub_graph):
    #this function gets a graph and a list of chosen vertices
    #and returns the sub-graph of only those vertices
    mat_size = len(index_sub_graph)
    mat = np.zeros((mat_size, mat_size))
    for i in range(mat_size):
        for j in range(mat_size):
            mat[i,j] = graph[index_sub_graph[i],index_sub_graph[j]]
    return mat

def count_motif(graph, motif):
    #this function gets a graph and a motif and counts how many
    #times this motif appears in the graph
    motif_size  = len(motif)
    graph_size = len(graph)
    nums_set = {i for i in range(graph_size)}
    index_sub_graphs =  findsubsets(nums_set, motif_size)
    count = 0
    flag = 0

    for i in range(len(index_sub_graphs)):
        pers = permutation(list(index_sub_graphs[i]))
        full_graphs = []
        for per in pers:
            mat = create_sub_graph(graph,per)
            for l in range(len(mat)):
                for k in range(len(mat)):
                    if motif[l,k] != mat[l,k] and motif[l,k] == 1:
                        flag = 1
            if flag == 0:
                full_graph = np.zeros((len(graph), len(graph)))
                for m in range(len(motif)):
                    for n in range(len(motif)):
                        full_graph[per[m],per[n]] = motif[m,n]
                #if not full_graph.all() in full_graphs:
                flag2 = 0
                for x in full_graphs:
                    if np.allclose(full_graph,x):
                        flag2 = 1
                if flag2 == 0:
                    full_graphs.append(full_graph)
                    count += 1
            flag = 0
    return count

def part1():
    #this function finds all the motifs of size n
    print("Please enter number: ")
    n = input()
    if n == "1":
        return []
    else:
        graphs = create_graphs(int(n))
        good_graphs = []
        for index, graph in enumerate(graphs):
            flag = 0
            if check_con(graph):
                for i in good_graphs:
                    if check_iso(graph, i):
                        flag = 1
                if flag == 0:
                    good_graphs.append(graph)
    return good_graphs

def part2(graph):
    #this function finds the number of occurrences of each motif in a graph
    good_graphs = part1()
    i = 0
    for motif in good_graphs:
        i += 1
        count = count_motif(graph, motif)
        print("#" + str(i) + ":")
        print(print_graph(motif))
        print("count=" + str(count)+"\n")

def string_to_graph(n,graph_string):
    edges = graph_string.split("(")
    graph = np.zeros((n, n))
    edges.remove("")

    for edge in edges:
        graph[int(edge[0]),int(edge[2])] = 1

    return graph


#main
flag = 0
while flag == 0:
    print("choose part (1 or 2): ")
    part = input()
    if part == '1':
        graphs = part1()
        print("count=" + str(len(graphs)))
        for i,graph in enumerate(graphs):
            print("#" + str(i) + ":")
            print(print_graph(graph)+"\n")


        flag = 1
    if part == '2':
        print("please enter number of nodes for graph: ")
        n = input()
        print("please enter graph: ")
        graph2 = input()

        graph2 = string_to_graph(int(n), graph2)
        part2(graph2)
        flag = 1

