from querys import Requests
from connection import connect


class UserApi:
    def __init__(self):
        self.request = Requests(connect)

    def login_user(self, username, password):
        return self.request.login_user(username, password)

    def register_user(self, username, email, password):
        return self.request.register_user(username, email, password)

    def get_drivers(self):
        return self.request.select_drivers()

    def get_customers(self):
        return self.request.select_customers()

    def get_cars(self):
        return self.request.select_cars()

    def get_contract(self):
        return self.request.select_contract()

    def get_invoice_id(self, invoice_id):
        return self.request.select_invoice_by_id(invoice_id)

    def get_ticket_id(self, ticket_id):
        return self.request.select_ticket_by_id(ticket_id)

    def get_info(self, contract_id):
        return self.request.select_info_by_id(contract_id)

    def insert_data_to_db(self, data_to_insert):
        return self.request.insert_data_cars(data_to_insert)