from v1.BonusCalculator import BonusCalculator
from v1.DataLoader import JSONDataLoader

data_loader = JSONDataLoader(json_file_path)
calculator = BonusCalculator(
    data_loader=data_loader,
    target_income=target_income)
calculator.load_data()
calculator.calculate()
calculator.print_result()
