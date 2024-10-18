from Utils.tools import Tools, CustomException
from Utils.querys import Querys
from Models.loan_model import LoanModel

class Loan():

    def __init__(self):
        self.tools = Tools()
        self.querys = Querys()
    
    # Function for create a loan to an client.
    def create_loan(self, data: dict):

        client_id = data['client_id']
        description = data['description']
        total_loan = data['total_loan']
        data_loan_save = dict()
        
        self.querys.check_client_by_id(client_id)
        
        """sumary_line
        
        Se comenta la funcion de validar limite ya que se correjira a futuro
        para que si sean 3 porque ahora mismo si ya pagó un prestamo aún lo
        cuenta como un prestamo activo
        """
        
        # quantity_loans = self.querys.validate_loan(client_id, True)
        # if quantity_loans >= 3:
        #     raise CustomException("Exceeds number of loans, maximum 3.")

        data_loan_save = {
            "client_id": client_id,
            "description": description.capitalize(),
            "total_loan": total_loan
        }
        self.querys.insert_data(LoanModel, data_loan_save)

        return self.tools.output(201, "Loan created successfully.")

    # Function for get all loans of client
    def show_loans_by_client(self, data: int):

        result = list()
        client_id = data["client_id"]

        loans = self.querys.validate_loan(client_id)
        
        if loans:
            for loan in loans:

                owe = loan.total_loan

                result_payments = self.querys.find_payments(loan.id)

                if len(result_payments) > 0:
                    result_difference = self.calculate_difference(result_payments)
                    owe = int(loan.total_loan) - result_difference

                result.append({
                    "id": loan.id,
                    "description": loan.description,
                    "total_loan": self.tools.format_currency(loan.total_loan),
                    "created_at": str(loan.created_at),
                    "payments": result_payments,
                    "owe": self.tools.format_currency(owe),
                })
                
        return self.tools.output(200, "Data found.", result)

    # Calculate the difference of the total loan and all payments 
    def calculate_difference(self, data: dict):

        result = 0
        for pay in data:
            result += pay['pay_amount']
        
        return result
