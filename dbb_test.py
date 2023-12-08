import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="youtube",
  password="youtubetest",
  database="database"
)

mycursor = mydb.cursor()

sql = "INSERT INTO product_result (name, img, url, price, created_at, search_text, source) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = [
  ('AMD Ryzen 5 3600 6-Core, 12-Thread Unlocked Desktop Processor with Wraith Stealth Cooler', 'https://m.media-amazon.com/images/I/51kKZ3R2eeL._AC_US40_.jpg', 'https://www.amazon.com//dp/B07STGGQ18', '99.50', '2023-09-30 14:02:36.132744', 'AMD Ryzen 5 3600 6-Core', 'https://www.amazon.com/'),
  ('AMD Ryzen 6 3600 6-Core, 12-Thread Unlocked Desktop Processor with Wraith Stealth Cooler', 'https://m.media-amazon.com/images/I/51kKZ3R2eeL._AC_US40_.jpg', 'https://www.amazon.com//dp/B07STGGQ18', '99.50', '2023-09-30 14:02:36.132744', 'AMD Ryzen 6 3600 6-Core', 'https://www.amazon.com/'),
  ('AMD Ryzen 7 3600 6-Core, 12-Thread Unlocked Desktop Processor with Wraith Stealth Cooler', 'https://m.media-amazon.com/images/I/51kKZ3R2eeL._AC_US40_.jpg', 'https://www.amazon.com//dp/B07STGGQ18', '99.50', '2023-09-30 14:02:36.132744', 'AMD Ryzen 7 3600 6-Core', 'https://www.amazon.com/')
]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")