from dataclasses import dataclass


@dataclass
class CorporatePolicy:
    min_amount: int
    max_amount: int
    value: str

    def __init__(self, input_policy_string=None):
        self.parse_policy(input_policy_string)

    def parse_policy(self, input_policy=None):
        if input_policy is not None:
            amounts, self.value = input_policy.split()
            min_amount_str, max_amount_str = amounts.split('-')
            self.min_amount = int(min_amount_str)
            self.max_amount = int(max_amount_str)


@dataclass
class PasswordDatabase:
    policy: CorporatePolicy
    password: str

    def check_corporate_policy(self):
        return self.policy.min_amount <= self.password.count(self.policy.value) <= self.policy.max_amount


if __name__ == '__main__':
    with open('passwords.txt') as f:
        policies = [PasswordDatabase(policy=CorporatePolicy(z[0].strip()), password=z[1].strip()) for z in
                    [y.split(':') for y in [x.strip() for x in f]]]
    valid_passwords = [x for x in policies if x.check_corporate_policy()]
    print('bagel')
