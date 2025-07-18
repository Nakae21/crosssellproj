import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from tqdm import tqdm  # pip install tqdm

# Update these credentials for your local PostgreSQL
DB_NAME = "crosssell_db"
DB_USER = "groupthree"
DB_PASS = "Group3@21"
DB_HOST = "localhost"
DB_PORT = "5432"

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

def load_and_insert(csv_path, insert_query, columns, chunksize=10000):
    print(f"Loading {csv_path} in chunks of {chunksize}...")
    total_rows = sum(1 for _ in open(csv_path, encoding='utf-8')) - 1  # total lines minus header
    chunks = total_rows // chunksize + 1
    reader = pd.read_csv(csv_path, chunksize=chunksize, encoding='utf-8')

    for chunk in tqdm(reader, total=chunks, unit='chunk'):
        values = [tuple(row[col] for col in columns) for _, row in chunk.iterrows()]
        execute_batch(cursor, insert_query, values)
        conn.commit()
    print(f"✅ Finished loading {csv_path}")

# Insert Departments
load_and_insert(
    'dataset/departments.csv',
    "INSERT INTO department (department_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
    ['department_id', 'department']
)

# Insert Aisles
load_and_insert(
    'dataset/aisles.csv',
    "INSERT INTO aisle (aisle_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
    ['aisle_id', 'aisle']
)

# Insert Products
load_and_insert(
    'dataset/products.csv',
    "INSERT INTO product (product_id, name, aisle_id, department_id) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
    ['product_id', 'product_name', 'aisle_id', 'department_id']
)

# Insert Orders
load_and_insert(
    'dataset/orders.csv',
    """INSERT INTO "order" (order_id, user_id, order_number, order_dow, order_hour_of_day, days_since_prior_order) 
       VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
    ['order_id', 'user_id', 'order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order']
)

cursor.close()
conn.close()

print("✅ All data loaded successfully into PostgreSQL!")
