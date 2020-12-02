from dataclasses import dataclass


@dataclass
class CorporatePolicy:
    first_index: int
    second_index: int
    value: str

    def __init__(self, input_policy_string=None):
        self.parse_policy(input_policy_string)

    def parse_policy(self, input_policy=None):
        if input_policy is not None:
            amounts, self.value = input_policy.split()
            first_index_str, second_index_str = amounts.split('-')
            self.first_index = int(first_index_str) - 1
            self.second_index = int(second_index_str) - 1


@dataclass
class PasswordDatabase:
    policy: CorporatePolicy
    password: str

    def check_corporate_policy(self):
        return (self.password[self.policy.first_index] == self.policy.value) ^ (self.password[
            self.policy.second_index] == self.policy.value)


if __name__ == '__main__':
    with open('passwords.txt') as f:
        policies = [PasswordDatabase(policy=CorporatePolicy(z[0].strip()), password=z[1].strip()) for z in
                    [y.split(':') for y in [x.strip() for x in f]]]
    valid_passwords = [x for x in policies if x.check_corporate_policy()]
    print('Valid Passwords Count: {}'.format(len(valid_passwords)))
