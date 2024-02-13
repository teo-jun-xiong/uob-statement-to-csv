END_STRING = ('------------------------------------------------------------ End of Transaction Details '
              '-------------------------------------------------------')


class Transaction:
    def __init__(self, date, description, difference, balance):
        self.date = date
        self.description = description.strip().replace(END_STRING, '')
        self.difference = difference
        self.balance = balance

    def __repr__(self):
        return (f"Transaction(date={self.date}, description={self.description}, difference={self.difference}, "
                f"balance={self.balance})")

    def to_tuple(self):
        return self.date, self.description, self.difference, self.balance
