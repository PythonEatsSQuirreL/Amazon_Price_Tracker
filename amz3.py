from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
import datetime

val = []
items = ["B07STGGQ18", "B07MFZY2F2", "B0143UM4TC"]

def feID(idx):
    iop = driver.find_element(By.ID, str(idx))
    return iop.text

#Create the Selenium instance with Edge and run it in background(consumes less resources than Chrome)
options = EdgeOptions()
options.add_argument('--headless')
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Edge(options=options)

for it in items:
    #Set the link for each item
    amz_link = "https://www.amazon.com//dp/" + str(it)

    #Open the browser page
    driver.get(amz_link)


    #WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='corePrice_feature_div']")))
    try:
        price = driver.find_element(By.ID, "corePriceDisplay_desktop_feature_div")
        price = str(price.text).replace("List Price:", "").replace("$", "")
        if "%" in price:
            price = price.split("%")[1].split()
            price = price[0] + "." + price[1]
        else:
            price = price.split()
            price = price[0] + "." + price[1]
        print("price: " + price)
    except:
        print("aici")
        price1 = driver.find_element(By.ID, "variation_style_name")
        print(str(price1.text))
        price2 = price1.find_element(By.ID, "a-autoid-15-announce")
        print(str(price2.text))
        price = price2.find_element(By.ID, "style_name_0_price")
        print(str(price.text))
        price4 = driver.find_element(By.ID, "style_name_0")
        print(str(price4.text))