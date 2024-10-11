import sqlite3
import io
from PIL import Image

conn = sqlite3.connect('Databases\\Product.db')
c = conn.cursor()

# Create products table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS products
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     image1 BLOB,
     image2 BLOB,
     image3 BLOB,
     image4 BLOB,
     image5 BLOB,
     name TEXT NOT NULL,
     price TEXT NOT NULL,
     description TEXT,
     username TEXT,
     email TEXT,
     sponsored INTEGER DEFAULT 0
)
''')

conn.commit()
c.close()  # Close cursor
conn.close()  # Close connection


def add_product(images, name, price, description, username, email):
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()

    # Convert images to binary format (up to 5 images)
    image_binaries = []
    for image in images:
        if image:
            image_data = io.BytesIO()
            image.save(image_data, format='PNG')
            image_binaries.append(image_data.getvalue())
        else:
            image_binaries.append(None)
    email = email[0] if isinstance(email, tuple) else email
    
    c.execute('''
        INSERT INTO products (image1, image2, image3, image4, image5, name, price, description, username, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (*image_binaries, name, price, description, username, email))

    conn.commit()
    c.close()  # Close cursor
    conn.close()  # Close connection

def resize_image(image, base_width=200):
    w_percent = base_width / float(image.size[0])
    h_size = int(float(image.size[1]) * float(w_percent))
    return image.resize((base_width, h_size), Image.LANCZOS)

def delete_products_by_username(username):
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()

    try:
        c.execute("DELETE FROM products WHERE username = ?", (username,))
        deleted_count = c.rowcount
        conn.commit()
        return deleted_count
    except Exception as e:
        print(f"Error deleting products: {e}")
        return 0
    finally:
        c.close()
        conn.close()

def is_sponsored(product_id):
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()
    c.execute("SELECT sponsored FROM products WHERE id = ?", (product_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else False

def make_sponsored(product_id):
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()
    c.execute("UPDATE products SET sponsored = 1 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def remove_sponsorship(product_id):
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()
    c.execute("UPDATE products SET sponsored = 0 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def fetch_products():
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()
    c.execute("SELECT id, image1, image2, image3, image4, image5, name, price, description, username, email, sponsored FROM products")
    products = c.fetchall()
    conn.close()
    return products

def fetch_sponsored_products():
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()
    c.execute("SELECT id, image1, image2, image3, image4, image5, name, price, description, username, email, sponsored FROM products WHERE sponsored = 1")
    sponsored_products = c.fetchall()
    conn.close()
    return sponsored_products

def fetch_other_products():
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()
    c.execute("SELECT id, image1, image2, image3, image4, image5, name, price, description, username, email, sponsored FROM products WHERE sponsored = 0")
    sponsored_products = c.fetchall()
    conn.close()
    return sponsored_products
