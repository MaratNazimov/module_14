import sqlite3

connection = sqlite3.connect("telegram_bot_sql.db")
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Buying(
    id INTEGER PRIMARY KEY,
    Product TEXT NOT NULL,
    Description TEXT,
    Price INTEGER NOT NULL,
    image BLOB)
    ''')

def convert(filename):
    with open(filename, 'rb') as file:
        read_f = file.read()
    return read_f

def bas(name, description, price, image):
    image = convert(image)
    cursor.execute("INSERT INTO Buying(Product, Description, Price, image) VALUES(?, ?, ?, ?)",
                   (name, description, price, image))

if __name__ == "__main__":
    initiate_db()
    bas("broccoli", "Полезный брокколи", 100, "img/broccoli.png")
    bas("apple", "Сочное яблоко", 200, "img/apple.png")
    bas("kiwi", "Вкусное киви", 300, "img/kiwi.png")
    bas("garnet", "Спелый гранат", 400, "img/garnet.png")
    connection.commit()
    connection.close()