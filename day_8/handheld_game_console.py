from dataclasses import dataclass
from typing import List

from parsimonious.grammar import Grammar, NodeVisitor

grammar = Grammar(r"""
    DOCUMENT    = LINE+
    LINE        = OPERATION
    
    OPERATION   = OPCODE spaces ARGUMENT newline?
    OPCODE      = 'acc' / 'jmp' / 'nop'
    ARGUMENT    = ~r"(\+|\-)\d+"
    spaces      = ~'\s*'
    newline     = ~"\n*"
""")


class OperationVisitor(NodeVisitor):
    def parse(self, *args, **kwargs):
        super().parse(*args, **kwargs)

    def visit_OPERATION(self, node, visited_children):
        return visited_children[0], visited_children[2]

    def visit_OPCODE(self, node, visited_children):
        return node.text

    def visit_ARGUMENT(self, node, visited_children):
        signed_int = int(node.text)
        return signed_int

    def generic_visit(self, node, visited_children):
        return visited_children or node


@dataclass
class Instruction:
    opcode: str
    argument: int
    times_called: int = 0


@dataclass
class GameConsole:
    instructions: List[Instruction]
    accumulator: int = 0

    def run(self):
        success = True
        i = 0
        while i < len(self.instructions):
            self.instructions[i].times_called += 1
            instruction = self.instructions[i]
            if instruction.times_called >= 2:
                success = False
                break
            elif instruction.opcode == 'acc':
                self.accumulator += instruction.argument
                i += 1
            elif instruction.opcode == 'jmp':
                if i + instruction.argument >= 0:
                    i += instruction.argument
                elif i + instruction.argument > len(self.instructions):
                    i = len(self.instructions)
                else:
                    i = 0
            elif instruction.opcode == 'nop':
                i += 1
            else:
                success = False
                break
        return success, self.accumulator


def main(file_name):
    tree = grammar.parse(open(file_name).read())

    ov = OperationVisitor()
    operations = ov.visit(tree)

    gc = GameConsole([Instruction(opcode, argument) for opcode, argument in operations])
    success, part_1_output = gc.run()

    print('Part 1 Outputs: Success - {} | Accumulator - {}'.format(success, part_1_output))

    for index, operation in enumerate(operations):
        loop_operations = operations.copy()
        if operation[0] == 'nop':
            y = list(operation)
            y[0] = 'jmp'
            loop_operations[index] = tuple(y)
        elif operation[0] == 'jmp':
            y = list(operation)
            y[0] = 'nop'
            loop_operations[index] = tuple(y)
        new_gc = GameConsole([Instruction(opcode, argument) for opcode, argument in loop_operations])
        success, attempt_output = new_gc.run()

        if success:
            print('Part 2 Outputs: Success - {} | Accumulator - {}'.format(success, attempt_output))
            break


if __name__ == '__main__':
    main('real_input.txt')
