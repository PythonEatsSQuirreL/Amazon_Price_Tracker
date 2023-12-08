from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import datetime
from selenium.webdriver.edge.options import Options as EdgeOptions
import sqlite3


val = []
items = ["B07STGGQ18", "B07MFZY2F2", "B0143UM4TC"]
DB_NAME = r"C:\Users\UNIX\Desktop\python projects\Price-Tracking-Web-Scraper-main\Price-Tracking-Web-Scraper-main\Backend\instance\database.db"

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
options.add_argument('--headless')
options.add_argument("--headless=new")
driver = webdriver.Edge(options=options)

for it in items:
    #Set the link for each item
    WIKI = "https://www.amazon.com//dp/" + str(it)

    #Open the browser page
    driver.get(WIKI)

    #Get the name
    t0 = driver.find_element(By.ID, "centerCol")
    t1 = t0.find_element(By.ID, "title_feature_div")
    t2 = t1.find_element(By.ID, "titleSection")
    t3 = t2.find_element(By.ID, "title")
    title = t3.find_element(By.ID, "productTitle")
    name = str(title.text)


    #Get the image source
    imgs = [my_elem.get_attribute("src") for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='altImages']/ul//li[@data-ux-click]//img")))]
    img = str(imgs[0])

    #Get the URL
    get_url = driver.current_url
    get_url = str(get_url)
    url = get_url

    #Get the price
    price = driver.find_element(By.ID, "corePrice_feature_div")
    price = str(price.text).strip(" ").strip("\n").strip("$")
    price = price.split()
    price = str(price[0] + "." +price[1])

    #Get the creation date
    created_at = datetime.datetime.now()

    #Get the searched text
    search_text = name.split(",")
    search_text = search_text[0]

    #Set the source
    source = "https://www.amazon.com/"

    #Print the values for debuging purposes
    #print(f"name: {name}\nimg: {img}\nurl: {url}\nprice: {price}\ncreated_at: {created_at}\nsearch_text: {search_text}\nsource: {source}")

    #Create a tuple with all the info
    xx = (name, img, url, price, created_at, search_text, source)

    #Add the tuple to the list
    val.append(xx)

    #Call the function that inserts the info to the table in the database
    populate_table()

    #Set the list to empty in order to populate it again with the info from the next product
    val = []

#delete_data_from_db("ryzen 5 36003")
#read_data_from_db()