import matplotlib

'''
SYNTAX TO RUN THE PROGRAM:

python ./graph_analysis.py graph_file.gml --components n --plot [C|N|P] --verify_homophily --verify_balanced_graph --output out_graph_file.gml

DESCRIPTION OF COMMANDS:

graph_file.gml:                 Input GML file representing the graph to analyze.
--components n:                 Partition the graph into n components (subgraphs/clusters).
--plot [C|N|P]:                 Plot the graph in different styles:
.                               C: Clustering coefficient.
.                               N: Neighborhood overlap.
.                               P: Color nodes by attribute or default.
--verify_homophily:             Test for homophily in the graph using a t-test 
.                               (nodes with the same color are  more likely to be connected).
--verify_balanced_graph:        Check if the graph is balanced based on edge signs.
--output out_graph_file.gml:    Save the updated graph with results to the specified output GML file.

'''