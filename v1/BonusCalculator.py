from .DataLoader import DataLoaderBase


class BonusCalculator(object):
    def __init__(self, data_loader: DataLoaderBase,  target_income: float):
        self.data_loader = data_loader
        self.target_income = target_income
        self.total_income = 0
        self.actual_income = 0

    def calculate_total_bonus(self, total_income, target_income=None):
        target_income = target_income if target_income else self.target_income
        percentage = float(total_income) / target_income
        if percentage < 1:
            return 0
        elif percentage >= 1 and percentage < 1.5:
            return 0.05 * total_income
        elif percentage >= 1.5 and percentage < 2:
            return 0.1 * total_income
        else:
            return 0.2 * total_income

    def load_data(self):
        data = self.data_loader.load_data()
        total_income = 0
        actual_income = 0
        for item in data:
            if item['type'] == 'order':
                total_income += float(item['amount'])
            elif item['type'] == 'income':
                actual_income += float(item['amount'])
        self.total_income = total_income
        self.actual_income = actual_income
        return total_income, actual_income

    def calculate(self):
        """
        :param data: a list of items that is either orders or incomes.
        Item format: 
             - 'type': a string, possible values: 'order', 'income'
             - 'amount': a float

        Return format:
            (
                total_income, 
                actual_income, 
                total_bonus, 
                actual_bonus
            )
        """
        self.total_bonus = self.calculate_total_bonus(self.total_income)

        self.actual_bonus = self.total_bonus * \
            (self.actual_income / self.total_income)

        return (
            self.total_income, self.actual_income,
            self.total_bonus, self.actual_bonus
        )

    def print_result(self):
        """
        Pretty print the result of the calculation.
        """
        print("Total income:    {:.2f}".format(self.total_income))
        print("Actual income:   {:.2f}".format(self.actual_income))
        print("Total bonus:     {:.2f}".format(self.total_bonus))
        print("Actual bonus:    {:.2f}".format(self.actual_bonus))
