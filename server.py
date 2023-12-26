from flask import Flask, request
from api import UserApi
from flask_cors import CORS
import csv
import io

application = Flask(__name__)
CORS(application)

api = UserApi()



@application.route("/drivers", methods=['GET'])
def get_products():
    return api.get_drivers()


@application.route("/customers", methods=['GET'])
def get_customers():
    return api.get_customers()


@application.route("/cars", methods=['GET'])
def get_cars():
    return api.get_cars()


@application.route("/contracts", methods=['GET'])
def get_contracts():
    return api.get_contract()


@application.route("/invoice/<int:invoice_id>", methods=['GET'])
def get_invoice(invoice_id):
    return api.get_invoice_id(invoice_id)


@application.route("/ticket/<int:ticket_id>", methods=['GET'])
def get_ticket(ticket_id):
    return api.get_ticket_id(ticket_id)


@application.route("/print/<int:contract_id>", methods=['GET'])
def get_info_print_document(contract_id):
    return api.get_info(contract_id)


@application.route("/import", methods=['POST'])
def import_data():
    try:
        file = request.files['file']

        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_data = csv.DictReader(stream)
        data_to_insert = [row for row in csv_data]

        success = api.insert_data_to_db(data_to_insert)

        if success:
            return "Данные успешно импортированы", 200
        else:
            return "Ошибка при импорте данных", 500

    except Exception as e:
        return f"Ошибка: {str(e)}", 500


if __name__ == "__main__":
    application.run(host='192.168.0.105', debug=True)
