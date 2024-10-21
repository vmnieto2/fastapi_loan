from Utils.tools import Tools
from Utils.querys import Querys
from Models.type_document_model import TypeDocumentModel
from Models.user_type_model import TypeUserModel

class Param:

    def __init__(self):
        self.tools = Tools()
        self.querys = Querys()

    def get_type_document(self):

        type_documents = self.querys.get_type_document()
        return self.tools.output(200, "Ok.", type_documents)

    def get_type_user(self):

        type_users = self.querys.get_type_user()
        return self.tools.output(200, "Ok.", type_users)

    def delete_param(self, data: dict):

        type_list = data["type_list"]
        param_id = data["param_id"]
        model = None

        if type_list == "get_type_document":
            model = TypeDocumentModel
        elif type_list == "get_type_user":
            model = TypeUserModel

        self.querys.delete_param(model, param_id)

        return self.tools.output(200, "Parameter deleted succesfully.")

    def update_param(self, data: dict):

        type_list = data["type_list"]
        param_id = data["param_id"]
        param_name = data["param_name"]
        param_description = data.get("param_description", '')
        model = None

        if type_list == "get_type_document":
            model = TypeDocumentModel
        elif type_list == "get_type_user":
            model = TypeUserModel

        self.querys.update_param(model, param_id, param_name, param_description)

        return self.tools.output(200, "Parameter updated succesfully.")

    def create_param(self, data: dict):

        type_list = data["type_list"]
        param_name = data["param_name"]
        param_description = data.get("param_description", '')
        model = None

        data_save = {
            'name': param_name
        }

        if type_list == "get_type_document":
            model = TypeDocumentModel
            data_save['description'] = param_description
        elif type_list == "get_type_user":
            model = TypeUserModel

        self.querys.create_param(model, data_save)

        return self.tools.output(200, "Parameter created succesfully.")
