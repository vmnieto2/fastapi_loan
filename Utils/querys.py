
from Config.db import session
from Utils.tools import Tools, CustomException
from Models.user_model import UserModel
from Models.type_document_model import TypeDocumentModel
from Models.user_type_model import TypeUserModel
from Models.client_model import ClientModel
from Models.loan_model import LoanModel
from Models.payment_model import PaymentModel

class Querys:

    def __init__(self):
        self.tools = Tools()

    # Query for obtain data of user to log
    def get_user(self, email: str):

        result = {}

        query = session.query(
            UserModel
        ).filter(
            UserModel.email == email, UserModel.status == 1,
        ).first()
        session.close()

        if not query:
            raise CustomException("User not found.")
        
        result = {
            "first_name": query.first_name,
            "last_name": query.last_name,
            "user_type_id": query.user_type_id,
            "password": query.password,
            "email": query.email,
        }

        return result
    
    # Query for have all type documents
    def get_type_document(self):

        response = list()
                
        query = session.query(
            TypeDocumentModel
        ).filter(
            TypeDocumentModel.status == 1
        ).all()
        session.close()
        
        if not query:
            raise CustomException("No data to show", 404)
        
        for key in query:
            response.append({
                "id": key.id,
                "name": key.name,
                "description": key.description
            })
        
        return response

    # Query for have all type users
    def get_type_user(self):

        response = list()
                
        query = session.query(
            TypeUserModel
        ).filter(
            TypeUserModel.status == 1
        ).all()
        session.close()
        
        if not query:
            raise CustomException("No data to show", 404)
        
        for key in query:
            response.append({
                "id": key.id,
                "name": key.name
            })
        
        return response

    # Query for have all clients
    def get_all_clients(self):

        response = list()

        query = session.query(
            ClientModel, TypeDocumentModel
        ).join(
            TypeDocumentModel,
            TypeDocumentModel.id == ClientModel.type_document
        ).filter(
            ClientModel.status == 1,
            TypeDocumentModel.status == 1
        ).all()
        session.close()

        if query:        
            for client, type_document in query:
                response.append({
                    "id": client.id,
                    "type_document": type_document.name,
                    "document": client.document,
                    "full_name": client.full_name.title(),
                    "cell_phone": client.cell_phone,
                    "email": client.email
                })
        
        return response

    # Function to verify if exists a field of any list of params
    def check_param_exists(self, model: any, param_to_find: int, field: str):

        query = session.query(
            model
        ).filter(
            model.id == param_to_find, model.status == 1
        ).first()
        session.close()

        msg = f"Field {field} doesn't exists."
        if not query:
            raise CustomException(msg)

        return True
    
    # Check if client exists.
    def check_if_exists_client(self, document: str):

        client = session.query(
            ClientModel
        ).filter(
            ClientModel.document == document, ClientModel.status == 1
        ).first()
        session.close()

        if client:
            raise CustomException("Client already exists.")
        
        return True
    
    # Inserting data.
    def insert_data(self, model: any, data: dict):
        
        try:
            client = model(data)
            session.add(client)
            session.commit()
            session.close()
        except Exception as ex:
            raise CustomException(str(ex))
        
        return True

    # Check if client exists by id.
    def check_client_by_id(self, client_id: int):

        client = session.query(
            ClientModel
        ).filter(
            ClientModel.id == client_id, ClientModel.status == 1
        ).first()
        session.close()

        if not client:
            raise CustomException("Client doesn't exists.")
        
        return True
    
    # Check quantity or data depending of the count variable.
    def validate_loan(self, client_id: int, count: bool = False):

        loans = session.query(
            LoanModel
        )
        if count:
            loans = loans.filter(
                LoanModel.client_id == client_id, LoanModel.status == 1
            ).count()
        else:
            loans = loans.filter(
                LoanModel.client_id == client_id, LoanModel.status.in_([1,2])
            ).all()
        session.close()
        
        return loans
    
    # Check if loan exists.
    def check_if_exists_loan(self, loan_id: int):

        result = None
        
        loan = session.query(
            LoanModel
        ).filter(
            LoanModel.id == loan_id, LoanModel.status == 1
        ).first()
        session.close()

        if not loan:
            raise CustomException("Loan doesn't exists.")
        
        result = {
            'id': loan.id,
            'client_id': loan.client_id,
            'description': loan.description,
            'total_loan': float(loan.total_loan)
        }
        
        return result

    # find payments by loan id
    def find_payments(self, loan_id: int):

        result = list()

        pays = session.query(
            PaymentModel
        ).filter(
            PaymentModel.loan_id == loan_id, PaymentModel.status == 1
        ).all()
        session.close()

        if pays:
            for pay in pays:
                result.append({
                    "id": pay.id,
                    "pay_amount": float(pay.pay_amount),
                    "pay_to_show": self.tools.format_currency(pay.pay_amount),
                    "created_at": str(pay.created_at)
                })

        return result

    # Function to find loan and change the status
    def change_status(self, loan_id: int, new_status: int):

        query = session.query(
            LoanModel
        ).filter(
            LoanModel.id == loan_id, LoanModel.status == 1
        ).first()

        if query:
            query.status = new_status
            session.commit()
        session.close()

        return True

    # Function to delete a param (change state)
    def delete_param(self, model, param_id):

        query = session.query(
            model
        ).filter(
            model.id == param_id, model.status == 1
        ).first()

        if not query:
            raise CustomException("Param doesn't exists.")

        query.status = 0
        session.commit()
        session.close()

        return True

    # Function to update a param
    def update_param(self, model, param_id, param_name, param_description):

        query = session.query(
            model
        ).filter(
            model.id == param_id, model.status == 1
        ).first()

        if not query:
            raise CustomException("Param doesn't exists.")

        query.name = param_name
        if param_description:
            query.description = param_description
        session.commit()
        session.close()

        return True
