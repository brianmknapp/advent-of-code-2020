from functools import reduce


def check_number_of_trees(forest, x_step, y_step):
    indices = [((x * y_step), (x * x_step) % len(forest[0])) for x in range(0, -(len(forest) // -y_step))]
    trees = [forest[l][i] for (l, i) in indices]
    return trees.count('#')


def main(file_name, steps):
    with open(file_name) as f:
        lines = [x.strip() for x in f]
        solutions = [check_number_of_trees(lines, l, i) for (l, i) in steps]
        solution = reduce(lambda a, b: a * b, solutions)
        print('Trees encountered: {}'.format(solution))


if __name__ == '__main__':
    main('real_input.txt', [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])
