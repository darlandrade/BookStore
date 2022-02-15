import psycopg2


def get_connection():
    return psycopg2.connect(host="localhost", user="postgres", password="postgres", database="bookstore")
