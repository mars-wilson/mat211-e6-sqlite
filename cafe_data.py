import sqlite3
import csv

def create_database():
    with sqlite3.connect('data/cafe.sqlite3') as s3:
        s3.execute(
            """CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY,
            name  TEXT NOT NULL,
            kind TEXT,
            volume REAL
            );
            """)
        s3.execute(
            """CREATE TABLE IF NOT EXISTS specials (
            id INTEGER PRIMARY KEY,
            date  TEXT NOT NULL,
            store_name TEXT NOT NULL,
            coffee_name TEXT,
            price REAL
            )
            """)
        s3.execute(
            """CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY,
            date  TEXT NOT NULL,
            store_name TEXT  NOT NULL,
            rating INTEGER NOT NULL
            )
            """)
        s3.execute(
            """CREATE TABLE IF NOT EXISTS coffees (
            id INTEGER PRIMARY KEY,
            name  TEXT NOT NULL,
            type TEXT,
            cost_lb REAL
            )
            """)


def drop_tables():
    with sqlite3.connect('data/cafe.sqlite3') as s3:
        s3.execute("DROP TABLE if exists coffees")
        s3.execute("DROP TABLE if exists specials")
        s3.execute("DROP TABLE if exists ratings")
        s3.execute("DROP TABLE if exists stores")

def load_cafe_data():
    with sqlite3.connect('data/cafe.sqlite3') as s3:
        with open('data/stores.csv') as csvfile:
            stores = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
            s3.executemany("""
             INSERT INTO STORES (name,kind,volume) values (:name, :kind, :volume )
            """, stores)
        with open('data/specials.csv') as csvfile:
            specials = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
            s3.executemany("""
             INSERT INTO SPECIALS (date,store_name,coffee_name,price) 
                values (:date, :store_name, :coffee_name, :price)
                """, specials)
        with open('data/ratings.csv') as csvfile:
            ratings = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
            s3.executemany("""
             INSERT INTO RATINGS (date,store_name,rating) 
                values (:date, :store_name, :rating)
                """, ratings)
        with open('data/coffees.csv') as csvfile:
            coffees = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
            s3.executemany("""
             INSERT INTO COFFEES (name,type,cost_lb) 
                values (:name, :type, :cost_lb)
                """, coffees)

if __name__=='__main__':
    drop_tables()
    create_database()
    load_cafe_data()
    print("Database created?")