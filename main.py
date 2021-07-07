from v1.BonusCalculator import BonusCalculator
from v1.DataLoader import JSONDataLoader

json_file_path = 'dummy_data.json'
target_income = 3000


def main():
    data_loader = JSONDataLoader(json_file_path)
    calculator = BonusCalculator(
        data_loader=data_loader,
        target_income=target_income)
    calculator.load_data()
    calculator.calculate()
    calculator.print_result()


if __name__ == '__main__':
    main()
