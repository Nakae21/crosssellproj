import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from tqdm import tqdm  # Ensure tqdm is installed

# DB connection config
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

def insert_order_products_from_iter(df_iter, total_rows, description):
    chunks = total_rows // 10000 + 1
    for chunk in tqdm(df_iter, total=chunks, desc=description, unit='chunk'):
        values = [
            (
                int(row['order_id']),
                int(row['product_id']),
                int(row['add_to_cart_order']),
                bool(row['reordered'])
            )
            for _, row in chunk.iterrows()
        ]
        execute_batch(cursor, """
            INSERT INTO order_product (order_id, product_id, add_to_cart_order, reordered)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, values)
        conn.commit()

# Count rows for progress tracking
train_total_rows = sum(1 for _ in open('dataset/order_products__train.csv')) - 1
prior_total_rows = sum(1 for _ in open('dataset/order_products__prior.csv')) - 1

print("Processing order_products__train.csv...")
train_iter = pd.read_csv('dataset/order_products__train.csv', chunksize=10000)
insert_order_products_from_iter(train_iter, train_total_rows, "order_products__train")

print("Processing order_products__prior.csv...")
prior_iter = pd.read_csv('dataset/order_products__prior.csv', chunksize=10000)
insert_order_products_from_iter(prior_iter, prior_total_rows, "order_products__prior")

cursor.close()
conn.close()

print("✅ order_product data inserted successfully.")
