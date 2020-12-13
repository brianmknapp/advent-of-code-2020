import itertools

from parsimonious.grammar import Grammar, NodeVisitor

grammar = Grammar(r"""
    DOCUMENT    = LINE+
    LINE        = VALUE
    
    VALUE       = NUMBER newline
    NUMBER      = ~r"\d+"
    newline     = ~"\n*"
""")


class ValueVisitor(NodeVisitor):
    def parse(self, *args, **kwargs):
        super().parse(*args, **kwargs)

    def visit_VALUE(self, node, visited_children):
        return visited_children[0]

    def visit_NUMBER(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children or node


def part_1(file_name, preamble_size):
    tree = grammar.parse(open(file_name).read())

    vv = ValueVisitor()
    values = vv.visit(tree)

    for i in range(preamble_size, len(values)):
        preamble = values[i - preamble_size:i]
        if not any([sum(s) == values[i] for s in itertools.product(preamble[::-1], repeat=2)]):
            return values[i]
    return None


def part_2(file_name, invalid_number):
    tree = grammar.parse(open(file_name).read())

    vv = ValueVisitor()
    values = vv.visit(tree)

    values_sets = [values[i:j] for i, j in itertools.combinations(range(len(values) + 1), 2) if len(values[i:j]) >= 2]

    sorted(values_sets, key=len)

    result = next(j for i, j in enumerate(values_sets) if sum(j) == invalid_number)

    return min(result), max(result)


if __name__ == '__main__':
    part_1_value = part_1('real_input.txt', 25)
    print('{} does not have a match'.format(part_1_value))

    part_2_lowest, part_2_highest = part_2('real_input.txt', part_1_value)
    print('Lowest: {} | Highest: {}'.format(part_2_lowest, part_2_highest))
    print('Sum of lowest + highest: {}'.format(sum([part_2_lowest, part_2_highest])))
