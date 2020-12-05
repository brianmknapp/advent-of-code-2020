from dataclasses import dataclass


@dataclass
class BoardingPass:
    data: str
    row: int = None
    column: int = None
    seat_id: int = None

    def calculate_seat(self, row_count, column_count):
        row_identifiers = self.data[:7]
        column_identifiers = self.data[-3:]
        self.calculate_row([*range(0, row_count)], row_identifiers)
        self.calculate_column([*range(0, column_count)], column_identifiers)
        self.calculate_seat_id(column_count)

    def calculate_row(self, row_range, identifiers):
        for i in identifiers:
            middle_index = len(row_range) // 2
            if i == 'F':
                row_range = row_range[:middle_index]
            elif i == 'B':
                row_range = row_range[middle_index:]
        self.row = row_range[0]

    def calculate_column(self, column_range, identifiers):
        for i in identifiers:
            middle_index = len(column_range) // 2
            if i == 'L':
                column_range = column_range[:middle_index]
            elif i == 'R':
                column_range = column_range[middle_index:]
        self.column = column_range[0]

    def calculate_seat_id(self, column_count):
        self.seat_id = self.row * column_count + self.column


def calculate_seat_id(row_number, column_count, column_number):
    return row_number * column_count + column_number


def find_empty_seats(boarding_passes, row_count, column_count):
    missing_seats = []
    all_seat_ids = [x['seat_id'] for x in boarding_passes]
    min_seat_id = min(all_seat_ids)
    max_seat_id = max(all_seat_ids)
    for i in range(0, row_count):
        for j in range(0, column_count):
            seat_id = calculate_seat_id(i, column_count, j)
            if seat_id not in all_seat_ids and min_seat_id <= seat_id <= max_seat_id:
                missing_seats.append(seat_id)
    for k in missing_seats:
        if k + 1 not in all_seat_ids and k - 1 not in all_seat_ids:
            missing_seats.remove(k)
    return missing_seats


def main(file_name, rows=128, columns=8):
    with open(file_name) as f:
        boarding_passes = [BoardingPass(x.strip()) for x in f]
        [x.calculate_seat(rows, columns) for x in boarding_passes]
        sorted_boarding_passes = sorted([x.__dict__ for x in boarding_passes], key=lambda item: item['seat_id'])
        missing_seats = find_empty_seats(sorted_boarding_passes, rows, columns)
        print('bagel')


if __name__ == '__main__':
    main('real_input.txt')
