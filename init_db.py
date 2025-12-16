import sqlite3

connection = sqlite3.connect("database.db")

with open("schema.sql") as f:
    connection.executescript(f.read())

cursor = connection.cursor()

def create_mock_data():
    cursor.execute("""
            INSERT INTO books (title, description, departure, picture, price, rate, country) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (
                       "Бійцівський клуб",
                       "роман про офісного працівника, що страждає від безсоння та споживацької кризи, який разом із харизматичним анархістом Тайлером Дерденом засновує таємний підпільний клуб, де чоловіки б'ються до крові, щоб відчути себе живими, вивільняючи первісну енергію та бунтуючи проти безглуздості сучасного світу та втрати мужності; це провокаційна історія про хаос, ідентичність та радикальну терапію, що переростає в небезпечну ідеологію.",
                       "kuiv",
                       "https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/3/8/38368_57777.jpg",
                       300,
                       "5",
                       "америка"))

    connection.commit()
    connection.close()

create_mock_data()