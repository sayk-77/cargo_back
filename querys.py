from flask import jsonify


class Requests:
    def __init__(self, connection):
        self.connect = connection


    def login_user(self, username, password):
        with self.connect.cursor() as cursor:
            cursor.execute('select user_password from users where user_login = %s ', (username,))
            row = cursor.fetchone()
            if row is not None:
                if password == row[0]:
                    return jsonify({'success': True, 'message': 'Успешно'})
                else:
                    return jsonify({'success': False, 'message': 'Не верный пароль'})

            return jsonify({'success': False, 'message': 'Пользователь не найден'})

    def register_user(self, username, email, password):
        with self.connect.cursor() as cursor:
            cursor.execute('insert into users (user_id, user_login, user_password, user_role, user_email)values (default, %s, %s, default, %s)', (username, password, email))
            self.connect.commit()
        return jsonify({'success': True}), 200

    def select_drivers(self):
        with self.connect.cursor() as cursor:
            cursor.execute('''
                        SELECT drivers.*, cars.car_model, cars.car_brands
                        FROM drivers
                        LEFT JOIN cars ON cars.car_id = drivers.driver_favorit_car
                        ORDER BY drivers.driver_id;
                    ''')
            response = cursor.fetchall()
            name_field = [desc[0] for desc in cursor.description]
            structure_date = []

            for row in response:
                date_descr = {name_field[i]: row[i] for i in range(len(name_field))}
                structure_date.append(date_descr)
        return structure_date

    def select_customers(self):
        with self.connect.cursor() as cursor:
            cursor.execute('select * from customers order by customer_id')
            response = cursor.fetchall()
            name_filed = [desc[0] for desc in cursor.description]
            structure_date = []

            for row in response:
                date_descr = {name_filed[i]: row[i] for i in range(len(name_filed))}
                structure_date.append(date_descr)
        return structure_date

    def select_cars(self):
        with self.connect.cursor() as cursor:
            cursor.execute('select * from cars order by car_id')
            response = cursor.fetchall()
            name_field = [desc[0] for desc in cursor.description]
            structure_date = []

            for row in response:
                date_descr = {name_field[i]: row[i] for i in range(len(name_field))}
                structure_date.append(date_descr)
        return structure_date

    def select_contract(self):
        with self.connect.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT 
                        contracts.*, 
                        TO_CHAR(contracts.contract_delivery_time, 'DD.MM.YYYY') AS formatted_delivery_date,
                        CONCAT(drivers.driver_last_name, ' ', drivers.driver_first_name, ' ', drivers.driver_midle_name) AS driver_name
                    FROM 
                        contracts
                    INNER JOIN 
                        drivers ON drivers.driver_id = contracts.contract_driver
                    ORDER BY 
                        contracts.contract_id;
                ''')
            response = cursor.fetchall()
            name_field = [desc[0] for desc in cursor.description]
            structure_date = []

            for row in response:
                date_descr = {name_field[i]: row[i] for i in range(len(name_field))}
                structure_date.append(date_descr)
        return structure_date

    def select_invoice_by_id(self, invoice_id):
        with self.connect.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    invoices.*, 
                    CONCAT(sender.customer_last_name, ' ', sender.customer_first_name, ' ', sender.customer_midle_name) AS sender_name,
                    CONCAT(recipient.customer_last_name, ' ', recipient.customer_first_name, ' ', recipient.customer_midle_name) AS recipient_name
                FROM invoices
                INNER JOIN customers AS sender ON invoices.invoice_sender = sender.customer_id
                INNER JOIN customers AS recipient ON invoices.invoice_recipient = recipient.customer_id
                WHERE invoice_id = %s
            ''', (invoice_id,))

            response = cursor.fetchall()
            name_field = [desc[0] for desc in cursor.description]

            for row in response:
                date_descr = {name_field[i]: row[i] for i in range(len(name_field))}
        return date_descr

    def select_ticket_by_id(self, ticket_id):
        with self.connect.cursor() as cursor:
            cursor.execute('''
                SELECT ticket.*, 
                CONCAT(drivers.driver_last_name, ' ', drivers.driver_first_name, ' ', drivers.driver_midle_name) AS driver_name,
                CONCAT(cars.car_brands, ' ', cars.car_model) AS car_info
                FROM traveltickets AS ticket
                JOIN drivers ON ticket.ticket_driver = drivers.driver_id
                JOIN cars ON ticket.ticket_car = cars.car_id
                WHERE ticket.ticket_id = %s;
            ''', (ticket_id,))

            response = cursor.fetchall()
            name_field = [desc[0] for desc in cursor.description]

            for row in response:
                date_descr = {name_field[i]: row[i] for i in range(len(name_field))}
        return date_descr

    def select_info_by_id(self, contract_id):
        with self.connect.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *,
                    concat(drivers.driver_last_name, ' ', drivers.driver_first_name, ' ', drivers.driver_midle_name) AS driver_name,
                    concat(sender_cust.customer_last_name, ' ', sender_cust.customer_first_name, ' ', sender_cust.customer_midle_name) AS sender_full_name,
                    concat(recipient_cust.customer_last_name, ' ', recipient_cust.customer_first_name, ' ', recipient_cust.customer_midle_name) AS recipient_full_name,
                    concat(cars.car_brands, ' ', cars.car_model) AS car_name
                    FROM contracts
                    JOIN invoices ON contracts.contract_invoice = invoices.invoice_id
                    JOIN traveltickets ON contracts.contract_travel_ticket = traveltickets.ticket_id
                    JOIN drivers ON contracts.contract_driver = drivers.driver_id
                    JOIN customers AS sender_cust ON invoices.invoice_sender = sender_cust.customer_id
                    JOIN customers AS recipient_cust ON invoices.invoice_recipient = recipient_cust.customer_id
                    JOIN cars ON traveltickets.ticket_car = cars.car_id
                    WHERE contracts.contract_id = %s
                ''', (contract_id,)
            )
            response = cursor.fetchall()
            name_field = [desc[0] for desc in cursor.description]

            for row in response:
                date_descr = {name_field[i]: row[i] for i in range(len(name_field))}
        return date_descr

    def insert_data_cars(self, data_to_insert):
        try:
            with self.connect.cursor() as cursor:
                for row in data_to_insert:
                    cursor.execute(
                        '''
                            INSERT INTO cars (car_model, car_brands, car_color, car_register_number, car_region_number, car_mileage, car_image) values (%s, %s, %s, %s, %s, %s, %s)
                        ''', (
                            row['car_model'], row['car_brand'], row['car_color'], row['car_registration_number'], row['car_region_number'], row['car_mileage'], row['car_image']
                        )
                    )
                return True
        except Exception as e:
            print(f"Ошибка при вставке данных: {str(e)}")
            return False
