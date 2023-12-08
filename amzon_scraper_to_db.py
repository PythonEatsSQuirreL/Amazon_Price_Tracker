from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
import sqlite3
import datetime

val = []
items = ["B09VCJ171S", "B07MFZY2F2", "B0143UM4TC"]
DB_NAME = r"C:\Users\PsychO\Desktop\100 milion dollar idea amazon\100 milion dollar idea amazon\Price-Tracking-Web-Scraper-main\Price-Tracking-Web-Scraper-main\Backend\instance\database.db"

def get_database_connection():
    """
    Connects to the database specified in 'DB_NAME'
    """
    con = sqlite3.connect(DB_NAME)
    return con

def populate_table():
    """
    Adds the data scraped from Amazon to the database
    """
    sql = '''INSERT INTO product_result (name, img, url, price, created_at, search_text, source) VALUES(?,?,?,?,?,?,?); '''
    con = get_database_connection()
    con.executemany(sql, val)
    con.commit()
    con.close()

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

#Create the Selenium instance with Edge and run it in background(consumes less resources than Chrome)
options = EdgeOptions()
#options.add_argument('--headless')
#options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])#exclude Devtools logs
driver = webdriver.Edge(options=options)

for it in items:
    #Set the link for each item
    amz_link = "https://www.amazon.com//dp/" + str(it)

    #Open the browser page
    driver.get(amz_link)

    #Get the name
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "centerCol")))
    title = driver.find_element(By.ID, "centerCol").find_element(By.ID, "title_feature_div").find_element(By.ID, "titleSection").find_element(By.ID, "title").find_element(By.ID, "productTitle")
    name = str(title.text)


    #Get the image source
    img = str([my_elem.get_attribute("src") for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='altImages']/ul//li[@data-ux-click]//img")))][0])

    #Get the URL
    url = str(driver.current_url)

    #Get the price
    try:
        price = driver.find_element(By.ID, "corePrice_feature_div")
        price = str(price.text).strip(" ").strip("\n").strip("$").split()
        price = str(price[0] + "." + price[1])
    except:
        price = driver.find_element(By.ID, "corePriceDisplay_desktop_feature_div")
        price = str(price.text).replace("List Price:", "").replace("$", "")
        if "%" in price:
            price = price.split("%")[1].split()
            price = price[0] + "." + price[1]
        else:
            price = price.split()
            price = price[0] + "." + price[1]

    #Get the creation date
    created_at = datetime.datetime.now()

    #Get the searched text
    search_text = name.split(",")[0]

    #Set the source
    source = "https://www.amazon.com/"

    #Create a tuple with all the info
    xx = (name, img, url, price, created_at, search_text, source)

    #Add the tuple to the list
    val.append(xx)

    #Call the function that inserts the info to the table in the database
    populate_table()

    #Set the list to empty in order to populate it again with the info from the next product
    val = []

