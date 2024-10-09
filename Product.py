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
     name TEXT,
     price TEXT,
     description TEXT,
     username TEXT,
     email TEXT)
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

def fetch_products():
    conn = sqlite3.connect('Databases\\Product.db')
    c = conn.cursor()

    c.execute("SELECT image1, image2, image3, image4, image5, name, price, description, username, email FROM products")
    products = c.fetchall()
    
    c.close()  # Close cursor
    conn.close()  # Close connection
    
    return products

def resize_image(image, base_width=200):
    w_percent = base_width / float(image.size[0])
    h_size = int(float(image.size[1]) * float(w_percent))
    return image.resize((base_width, h_size), Image.LANCZOS)