import os
import mysql.connector as mysql
import auth
from decouple import config

# load_dotenv('.env')
# db = mysql.connect(
#         host=config('HOST'),
#         user=config('USERNAME'),
#         password=config('PASS'),
#         database=config('DB')
#     )
def connect():
    db = mysql.connect(
            host=auth.HOST,
            user=auth.USERNAME,
            password=auth.PASS,
            database=auth.DB
        )
    print("Connected to database")
    return db

def insert(db, stock_industry, stock_market, stock_name, stock_market_cap, stock_symbol):
    cursor = db.cursor()
    query = "INSERT INTO stock (stock_industry, stock_market, stock_name, stock_market_cap, stock_symbol) VALUES (%s, %s, %s, %s, %s)"
    values = (stock_industry, stock_market, stock_name, stock_market_cap, stock_symbol)
    cursor.execute(query, values)
    db.commit()
    print(cursor.rowcount, "record inserted.")

def select_by_symbol(db, stock_symbol):
    cursor = db.cursor()
    query = "SELECT * FROM stock WHERE stock_symbol = %s"
    values = (stock_symbol,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    columns = cursor.description
    result = [dict(zip([column[0] for column in columns], row)) for row in result]

    return result

def select_by_id(db, id):
    cursor = db.cursor()
    query = "SELECT * FROM stock WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    columns = cursor.description
    result = [dict(zip([column[0] for column in columns], row)) for row in result]

    return result

def select_all(db):
    cursor = db.cursor()
    query = "SELECT * FROM stock"
    cursor.execute(query)
    result = cursor.fetchall()
    columns = cursor.description
    result = [dict(zip([column[0] for column in columns], row)) for row in result]

    return result

def delete_by_symbol(db, stock_symbol):
    cursor = db.cursor()
    query = "DELETE FROM stock WHERE stock_symbol = %s"
    values = (stock_symbol,)
    cursor.execute(query, values)
    db.commit()
    print(cursor.rowcount, "record(s) deleted")

def delete_all(db):
    cursor = db.cursor()
    query = "DELETE FROM stock"
    cursor.execute(query)
    db.commit()
    print(cursor.rowcount, "record(s) deleted")

def update_by_symbol(db, stock_industry, stock_market, stock_name, stock_market_cap, stock_symbol):
    cursor = db.cursor()
    query = "UPDATE stock SET stock_industry = %s, stock_market = %s, stock_name = %s, stock_market_cap = %s WHERE stock_symbol = %s"
    values = (stock_industry, stock_market, stock_name, stock_market_cap, stock_symbol)
    cursor.execute(query, values)
    db.commit()
    print(cursor.rowcount, "record(s) affected")

def update_all(db, stock_industry, stock_market, stock_name, stock_market_cap):
    cursor = db.cursor()
    query = "UPDATE stock SET stock_industry = %s, stock_market = %s, stock_name = %s, stock_market_cap = %s"
    values = (stock_industry, stock_market, stock_name, stock_market_cap)
    cursor.execute(query, values)
    db.commit()
    print(cursor.rowcount, "record(s) affected")

def close(db):
    db.close()
    print("Connection closed")

# connect()
# print(select_all(connect()))