import json


def two_entries_that_sum(expense_list, desired_sum):
    for i, number in enumerate(expense_list[:-1]):
        complementary = desired_sum - number
        if complementary in expense_list[i + 1:]:
            return number, complementary


def three_entries_that_sum(expense_list, desired_sum):
    for i, first_number in enumerate(expense_list[:-1]):
        for j, second_number in enumerate(expense_list[:-1]):
            complementary = desired_sum - first_number - second_number
            if complementary in expense_list:
                return first_number, second_number, complementary


if __name__ == '__main__':
    with open('day1part1.json') as json_file:
        data = json.load(json_file)
    value_one, value_two = two_entries_that_sum(data, 2020)
    print('{} * {} = {}'.format(value_one, value_two, value_one * value_two))

    part_2_value_one, part_2_value_two, part_2_value_three = three_entries_that_sum(data, 2020)
    print('{} * {} * {} = {}'.format(part_2_value_one, part_2_value_two, part_2_value_three, part_2_value_one * part_2_value_two * part_2_value_three))

