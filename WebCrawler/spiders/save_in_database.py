import mysql.connector as mc

db = mc.connect(
    host="localhost",
    user="root",
    password="Azerty94",
    database="webscraping"
)

cursor = db.cursor()

def save_in_database(item):
    sql = "INSERT INTO `webscraping`.`allocine` (`title`, `img`, `author`, `time`, `genre`, `score`, `desc`, `release`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (item['title'], item['img'], item['author'], item['time'], item['genre'], item['score'], item['desc'], item['release'])
    cursor.execute(sql, val)
    db.commit()