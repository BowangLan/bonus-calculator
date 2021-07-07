import datetime


class MonthOrderList(object):
    def __init__(self, target_income):
        self.target_income = target_income
        self.order_list = []
        self.estimated_income = 0
        self.actual_income = 0
        self.bonus_sum = 0
        self.total_bonus = 0
        self.data = None

    def calculate_total_bonus(self):
        self.total_bonus = 0


class Order(object):
    def __init__(self, parent_month: MonthOrderList = None,  amount: int = 0, date: datetime.date = None):

        self.parent_month = parent_month
        self.amount = amount
        self.date = date

        self._bonus = 0
        self.paid_status = False

    @property
    def percentage(self):
        return self.parent_month.total

    @property
    def bonus(self):
        return

    def get_bonus(self):
        return self._bonus if self.paid_status else 0

    def paid(self):
        self.paid_status = True


""" assume each item in data is a Python dictionary with the following structure:
{ 
  'type': 'order' or 'income',
  'amount': some number,
  'date': date
}
"""


class BonusSumCalculator(object):
    def __init__(self, target_income):
        self.target_income = target_income
        self.order_list = []
        self.estimated_income = 0
        self.actual_income = 0
        self.bonus_sum = 0
        self.data = None

    def load_data(self, data_path):
        """
        After executing this method, the estimated income and the actual income is calculated from the data file specified.
        """
        with open(data_path) as f:
            self.data = f.read()

        for item in self.data:
            self.parse_item(item)

    def parse_item(self, item):
        if item['type'] == 'order':
            order = Order(amount=item['amount'])
            self.order_list.append(order)
            self.estimated_income += float(item['amount'])
        elif item['type'] == 'income':
            self.actual_income += float(item['amount'])

    def calculate(self):
        """
        Logic
        """
        # calculate the total bonus
        total_bonus = self._calculate_total_bonus()
        for order in self.order_list:

        return self.bonus_sum

    def _calculate_total_bonus(self):
        """
        Calculate the bonus according to certain rules.

        Calculating rules:
        - 100% - 150% = $5
        - 150% - 200% = 10
        - 200% up = 15
        """
        if self.estimated_income < self.target_income:
            return 0
        else:
            pass


def main():

    # load the dataset from a file source
    data_path = ''
    calculator = BonusSumCalculator()
    calculator.load_data(data_path)
    calculator.calcualte()
    print("Output: {}".format(calculator.bonus_sum))


if __name__ == '__main__':
    main()
