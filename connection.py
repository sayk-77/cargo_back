import psycopg2

connect = psycopg2.connect(
    database="CargoTransportation",
    user="st1991",
    password="pwd1991",
    host="172.20.7.8",
    port="5432"
)
