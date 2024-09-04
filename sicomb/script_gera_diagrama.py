import pydot

(graph,) = pydot.graph_from_dot_file('meu_diagrama.dot')
graph.set_graph_defaults(dpi=500)
graph.write_png('diagrama_classes.png')
graph.write_pdf('diagrama_classes.pdf')