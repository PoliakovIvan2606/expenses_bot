import sqlite3


def create_connect():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        return cur


def get_dict_categories():
    cur = create_connect()

    data = cur.execute('''
                SELECT * FROM categories;
                ''')

    return data.fetchall()
def add_category(codename: str, name: str):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
                INSERT INTO categories (codename, name) 
                VALUES (?, ?)
                ''', (codename, name))
    conn.commit()
    conn.close()

def add_data_db(name: str, price: int | float, category_name: str):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
                INSERT INTO products (name, price, category_name)
                VALUES (?, ?, ?)
                ''', (name, price, category_name))
    conn.commit()
    conn.close()

def get_dict_products():
    cur = create_connect()

    data = cur.execute('''
    SELECT products.id, products.name, products.price, categories.name AS category_name
    FROM products
    JOIN categories ON products.category_name = categories.codename;
    ''')
    data = data.fetchall()
    db = {}
    for product in data:
        if db.get(product[3]) is not None:
           db[product[3]].append((product[0], product[1], product[2]))
        else:
            db[product[3]] = [(product[0], product[1], product[2])]

    return db

def del_product(product_id: int):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('DELETE FROM products WHERE id = ?', (product_id,))
    
    conn.commit()
    conn.close()

def add_income(name: str, price: int | float):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
                INSERT INTO income (name, price)
                VALUES (?, ?)
                ''', (name, price))
    conn.commit()
    conn.close()

def get_income():
    cur = create_connect()

    data = cur.execute('''
    SELECT name, price FROM income;
    ''')
    data = data.fetchall()
    return data
