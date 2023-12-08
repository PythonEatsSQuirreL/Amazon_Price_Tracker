#Manipulate the scraped data from the database
import sqlite3
import datetime

DB_NAME = r"C:\Users\PsychO\Desktop\100 milion dollar idea amazon\100 milion dollar idea amazon\Price-Tracking-Web-Scraper-main\Price-Tracking-Web-Scraper-main\Backend\instance\database.db"

def get_database_connection():
    """
    Connects to the database specified in 'DB_NAME'
    """
    con = sqlite3.connect(DB_NAME)
    return con

def read_data_from_db():
    """
    Return from the database the name and the price 
    of the products scraped today from database.
    """
    sql_query = "SELECT name, price FROM product_result WHERE created_at LIKE ? || '%'"
    tdy = str(datetime.datetime.today().date())
    con = get_database_connection()
    cur = con.cursor()
    cur.execute(sql_query, (tdy,))
    results = cur.fetchall()
    cur.close()
    con.close()
    for res in results:
        print(str(res).strip("(").strip(")").strip(",").replace("'", "") + "$")
    return results

def delete_data_from_db(name):
    """
    Delete selected data from database.
    execute the given sql statement to remove
    the lines where the value "name" equals the given value
    """
    sql_query = "DELETE from product_result WHERE name = ?"
    con = get_database_connection()
    con.execute(sql_query, (name,))
    con.commit()
    con.close()

#delete_data_from_db("ryzen 5 36003")
read_data_from_db()