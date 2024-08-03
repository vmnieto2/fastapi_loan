from Utils.tools import Tools
from Utils.querys import Querys
from Models.type_document_model import TypeDocumentModel
from Models.client_model import ClientModel

class Client:

    def __init__(self):
        self.tools = Tools()
        self.querys = Querys()

    # Function for have all active clients
    def get_all_clients(self):
                
        clients = self.querys.get_all_clients()
        
        if not clients:
            return self.tools.output(200, "No data to show.")
        
        return self.tools.output(200, "Data found", clients)
    
    # Function for save a client.
    def save_client(self, data: dict):
        
        # Get all params
        type_document = data['type_document']
        document = data['document']
        first_name = data['first_name']
        second_name = data['second_name']
        last_name = data['last_name']
        second_last_name = data['second_last_name']
        cell_phone = data['cell_phone']
        email = data['email']
        data_client_save = None
        
        # Validate if param exists
        type_document_model = TypeDocumentModel
        type_document_field = "tipo documento"
        
        """
            Structure of this funcion is
            1. model name
            2. param to find in model
            3. current field name in json
        """
        self.querys.check_param_exists(
            type_document_model, type_document, type_document_field
        )
        
        # Validate if client exists
        self.querys.check_if_exists_client(document)

        # concat full name
        full_name = " ".join(x for x in [first_name, second_name, last_name, second_last_name] if x)
        
        # json of client data to save
        data_client_save = {
            'type_document': type_document,
            'document': document,
            'first_name': first_name,
            'second_name': second_name,
            'last_name': last_name,
            'second_last_name': second_last_name,
            'full_name': full_name,
            'cell_phone': cell_phone,
            'email': email
        }
        self.querys.insert_data(ClientModel, data_client_save)

        return self.tools.output(201, "Client created successfully.")
