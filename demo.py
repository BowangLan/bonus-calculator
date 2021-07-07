from v1.BonusCalculator import BonusCalculator
from v1.DataLoader import JSONDataLoader

json_file_path = 'dummy_data.json'
target_income = 3000

data_loader = JSONDataLoader(data_path=json_file_path)
calculator = BonusCalculator(
    data_loader=data_loader,
    target_income=target_income)
calculator.load_data()
calculator.calculate()
calculator.print_result()
