from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import datetime
from selenium.webdriver.edge.options import Options as EdgeOptions
# Initialize the webdriver
fob = open(r"C:\Users\UNIX\Desktop\python projects\builds download\build_names.txt", "a")



options = EdgeOptions()
options.add_argument('--headless')
options.add_argument("--headless=new")
driver = webdriver.Edge(options=options)
build_names = []
WIKI = "https://www.amazon.com//dp/B07STGGQ18"
driver.get(WIKI)
t0 = driver.find_element(By.ID, "centerCol")
#print(t0.text)
t1 = t0.find_element(By.ID, "title_feature_div")
#print(t1.text)
t2 = t1.find_element(By.ID, "titleSection")
#print(t2.text)
t3 = t2.find_element(By.ID, "title")
#print(t3.text)
title = t3.find_element(By.ID, "productTitle")

#print(title.text)


imgs = [my_elem.get_attribute("src") for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='altImages']/ul//li[@data-ux-click]//img")))]
#print(imgs[0])

get_url = driver.current_url
get_url = str(get_url)
#print(get_url)

price = driver.find_element(By.ID, "corePrice_feature_div")
price = str(price.text).strip(" ").strip("\n").strip("$")
price = price.split()
#print(price[0] + "." +price[1])

#print([x for x in range(2, 5)])
name = str(title.text)
img = str(imgs[0])
url = get_url
price = str(price[0] + "." +price[1])
created_at = datetime.datetime.now()
search_text = name.split(",")
search_text = search_text[0]
source = "https://www.amazon.com/"

print(f"name: {name}\nimg: {img}\nurl: {url}\nprice: {price}\ncreated_at: {created_at}\nsearch_text: {search_text}\nsource: {source}")