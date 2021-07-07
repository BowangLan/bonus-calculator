from v1.BonusCalculator import BonusCalculator
from v1.DataLoader import UserInputDataLoader


def main():
    target_income = float(input("Enter target income: "))
    user_input_data_loader = UserInputDataLoader()
    calculator = BonusCalculator(
        data_loader=user_input_data_loader,
        target_income=target_income)
    calculator.load_data()
    try:
        calculator.calculate()
        calculator.print_result()
    except Exception:
        print("An error occured duing calculation")


if __name__ == '__main__':
    main()
