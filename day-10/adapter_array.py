from collections import defaultdict

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


def part_1(file_name):
    tree = grammar.parse(open(file_name).read())

    vv = ValueVisitor()
    values = vv.visit(tree)

    values.append(0)
    values.append(max(values) + 3)

    differences = {
        '1-jolt': 0,
        '2-jolt': 0,
        '3-jolt': 0
    }

    values.sort()

    for i, j in enumerate(values):
        try:
            difference = values[i + 1] - j

            if difference is 1:
                differences['1-jolt'] += 1
            elif difference is 2:
                differences['2-jolt'] += 1
            elif difference is 3:
                differences['3-jolt'] += 1
        except IndexError:
            pass

    return differences


def part_2(file_name):
    paths = defaultdict(int)
    paths[0] = 1

    tree = grammar.parse(open(file_name).read())

    vv = ValueVisitor()
    values = vv.visit(tree)

    values.append(0)
    values.append(max(values) + 3)

    values.sort()

    for adapter in values:
        for diff in range(1, 4):
            next_adapter = adapter + diff
            if next_adapter in values:
                paths[next_adapter] += paths[adapter]

    return paths


if __name__ == '__main__':
    part_1_result = part_1('real_input.txt')

    print('{} 1-jolt differences multiplied by {} 3-jolt differences = {}'.format(part_1_result['1-jolt'],
                                                                                  part_1_result['3-jolt'], (
                                                                                          part_1_result['1-jolt'] *
                                                                                          part_1_result['3-jolt'])))

    part_2_result = part_2('real_input.txt')

    print('debug')
