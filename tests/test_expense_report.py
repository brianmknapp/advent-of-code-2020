import pytest

from expense_report import expense_report


def test_main():
    first_number, second_number = expense_report.two_entries_that_sum([1721, 979, 366, 299, 675, 1456], 2020)
    assert first_number == 1721
    assert second_number == 299
