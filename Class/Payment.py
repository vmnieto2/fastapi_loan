from Utils.tools import Tools, CustomException
from Utils.querys import Querys
from Models.payment_model import PaymentModel

class Payment():

    def __init__(self):
        self.tools = Tools()
        self.querys = Querys()
    
    # Function for create a loan to an client.
    def create_payment(self, data: dict):

        loan_id = data['loan_id']
        pay_amount = data['pay_amount']
        data_pay_save = {}
        owe = 0
        
        result_loan = self.querys.check_if_exists_loan(loan_id)
        
        total_loan = result_loan['total_loan']

        result_payments = self.querys.find_payments(loan_id)
        if len(result_payments) > 0:
            sum_result = self.calculate_difference(result_payments)

            owe = total_loan - sum_result

            if pay_amount > owe:
                msg = "The amount to pay is higher than what is owed."
                raise CustomException(msg)
            
            if sum_result == total_loan:
                return self.tools.output(200, "The debt is already paid.")

        if pay_amount > total_loan:
            msg = "The amount to pay is higher than the total of loan."
            raise CustomException(msg)
        elif pay_amount <= 0:
            msg = "The amount to pay is invalid."
            raise CustomException(msg)

        data_pay_save = {
            "loan_id": loan_id,
            "pay_amount": pay_amount
        }
        self.querys.insert_data(PaymentModel, data_pay_save)
        
        return self.tools.output(201, "Payment created successfully.")

    # Function for get all pays of a specific loan
    def show_payments(self, data: int):

        loan_id = data['loan_id']
        response = dict()

        result_loan = self.querys.check_if_exists_loan(loan_id)
        
        total_loan = result_loan['total_loan']
        owe = result_loan['total_loan']
        
        result_payments = self.querys.find_payments(loan_id)

        if len(result_payments) > 0:
            result_difference = self.calculate_difference(result_payments)
            owe = total_loan - result_difference

        response = {
            'payment_list': result_payments,
            'owe': owe,
        }

        return self.tools.output(200, "Data found.", response)

    # Calculate the difference of the total loan and all payments 
    def calculate_difference(self, data: dict):

        result = 0
        for pay in data:
            result += pay['pay_amount']
        
        return result
