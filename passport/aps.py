import re
from dataclasses import dataclass


@dataclass
class Passport:
    byr: str = None
    iyr: str = None
    eyr: str = None
    hgt: str = None
    hcl: str = None
    ecl: str = None
    pid: str = None
    cid: str = None

    def is_valid(self):
        return all([self.is_byr_valid(),
                    self.is_iyr_valid(),
                    self.is_eyr_valid(),
                    self.is_hgt_valid(),
                    self.is_hcl_valid(),
                    self.is_ecl_valid(),
                    self.is_pid_valid()
                    ])

    def is_byr_valid(self):
        try:
            return re.search(r"^(19[2-9][0-9]|20[0][0-2])$", self.byr) is not None
        except TypeError:
            return False

    def is_iyr_valid(self):
        try:
            return re.search(r"^(20[1][0-9]|2020)$", self.iyr) is not None
        except TypeError:
            return False

    def is_eyr_valid(self):
        try:
            return re.search(r"^(20[2][0-9]|2030)$", self.eyr) is not None
        except TypeError:
            return False

    def is_hgt_valid(self):
        try:
            return re.search(r'^((1[5-8][0-9]cm|19[0-3]cm)|(59in|6[0-9]in|7[0-6]in))$', self.hgt) is not None
        except TypeError:
            return False

    def is_hcl_valid(self):
        if self.hcl is not None:
            return re.search(r'^#[0-9a-f]{6}$', self.hcl) is not None
        else:
            return False

    def is_ecl_valid(self):
        if self.ecl is not None:
            return self.ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        else:
            return False

    def is_pid_valid(self):
        if self.pid is not None:
            return re.search(r'^\d{9}$', self.pid) is not None
        else:
            return False


def main(file_name):
    with open(file_name) as f:
        passports = []
        current_passport = Passport()
        while True:
            line = f.readline()
            if not line:
                passports.append(current_passport)
                print('eof')
                break
            if line == '\n':
                passports.append(current_passport)
                current_passport = Passport()
                continue
            else:
                passport_dict = dict(x.split(':') for x in line.split())
                for k, v in passport_dict.items():
                    current_passport.__setattr__(k, v)

        passport_dicts = [{'actual': x, 'validity': x.is_valid()} for x in passports]

        print('Valid Passports: {} / {}'.format([x.is_valid() for x in passports].count(True), len(passports)))


if __name__ == '__main__':
    main('real_input.txt')
