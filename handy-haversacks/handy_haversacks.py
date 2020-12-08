from parsimonious.grammar import Grammar, NodeVisitor
import networkx as nx

grammar = Grammar(r"""
    DOCUMENT    = LINE+
    LINE        = (ENTRY / TERMINAL)
    
    TERMINAL    = PARENT "no other bags." "\n"?
    ENTRY       = PARENT CHILDREN "." "\n"?
    
    PARENT      = COLOR " bags contain "
    CHILDREN    = CHILD+
    CHILD       = NUMBER " " COLOR " " BAGBAGS SEPARATOR
    
    NUMBER      = ~r"\d+"
    COLOR       = ~r"\w+ \w+"
    BAGBAGS     = ("bags" / "bag")
    SEPARATOR   = ~r"(, |(?=\.))"
""")


class BagVisitor(NodeVisitor):
    graph = None

    def parse(self, *args, **kwargs):
        self.graph = nx.DiGraph()
        super().parse(*args, **kwargs)
        return self.graph

    def visit_ENTRY(self, node, visited_children):
        parent, children, *_ = visited_children
        for count, child in children:
            self.graph.add_edge(parent, child, count=count)

    def visit_PARENT(self, node, visited_children):
        return visited_children[0]

    def visit_CHILD(self, node, visited_children):
        return (visited_children[0], visited_children[2])

    def visit_COLOR(self, node, visited_children):
        self.graph.add_node(node.text)
        return node.text

    def visit_NUMBER(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def main(file_name):
    bv = BagVisitor()
    bv.grammar = grammar

    graph = bv.parse(open(file_name).read())

    print('Bags that can eventually contain at least one shiny gold bag: {}'.format(
        len(nx.ancestors(graph, 'shiny gold'))))

    def get_count(parent):
        return 1 + sum(get_count(child) * graph.edges[parent, child]["count"] for child in graph.neighbors(parent))

    print('Number of bags required inside of a single shiny gold bag : {}'.format(get_count('shiny gold') - 1))


if __name__ == '__main__':
    main('real_input.txt')
