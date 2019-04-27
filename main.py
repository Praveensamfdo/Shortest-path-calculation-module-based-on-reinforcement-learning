import reinf_shortest

graph = reinf_shortest.QlearnShortest()

# adding nodes
graph.add_node(1)
graph.add_node(2)
graph.add_node(3)
graph.add_node(4)
graph.add_node(5)
graph.add_node(6)
graph.add_node(7)
graph.add_node(8)
graph.add_node(9)
graph.add_node(10)
graph.add_node(11)

# adding edges
graph.add_edge(1, 2, 9)
graph.add_edge(2, 3, 75)
graph.add_edge(3, 5, 45)
graph.add_edge(5, 9, 32)
graph.add_edge(9, 11, 76)
graph.add_edge(11, 10, 58)
graph.add_edge(10, 7, 23)
graph.add_edge(7, 8, 96)
graph.add_edge(8, 6, 150)
graph.add_edge(6, 4, 12)
graph.add_edge(4, 1, 24)
graph.add_edge(2, 4, 34)
graph.add_edge(6, 5, 65)
graph.add_edge(8, 9, 122)

sh, Q, exec_time, R = graph.calcshortest(2, 9)

print("%s\n" % R)
print("%s\n" % Q)
print("%s\n" % sh)
print("%s\n" % exec_time)