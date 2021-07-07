import json


class DataLoaderBase(object):
    def __init__(self, data_path: str = None, **kwargs):
        self.data_path = data_path

        # default arguments for open()
        kwargs['encoding'] = 'utf-8'
        self.kwargs = kwargs

    def load_data(self) -> list:
        pass


class JSONDataLoader(DataLoaderBase):

    def load_data(self):
        with open(self.data_path, **self.kwargs) as f:
            data = json.load(f)
        return data


class UserInputDataLoader(DataLoaderBase):

    INSTRUCTIONS = """Instructions for entering data:
    - to enter an order data, enter "o <amount>" without the double quotation. 
    Example: "o 3000" means an order of 3000 Yuan.
    - to enter an income data, data "i <amount>" without the double quotation. 
    Example: "i 2000" means an income of 2000 Yuan.
    Notice that the work "income" and the amount must be separated by a space.
    - enter "q" without double quotation to exit the data entering phase and calculate the bonus.
    """

    def load_data(self):
        print(self.INSTRUCTIONS)
        input_data = []
        while True:
            user_input = input("Enter data: ").strip()
            if user_input == 'q':
                break
            user_input = user_input.split(' ')
            try:
                if user_input[0] == 'o':
                    data_type = 'order'
                elif user_input[0] == 'i':
                    data_type = 'income'
                else:
                    raise Exception
            except Exception as e:
                print("Invalid input value")
                print(e)
                continue
            amount = float(user_input[1])
            print('Data entered: type: {}; amount: {}'.format(
                data_type, amount
            ))
            input_data.append({
                'type': data_type,
                'amount': amount
            })
        return input_data
