import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def get_connection(dbname=None):
    return psycopg2.connect(
        database=dbname or DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def create_database_if_not_exists():
    conn = get_connection("defaultdb")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database '{DB_NAME}' created.")

    conn.close()


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS producers (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS colors (
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR(30) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR(30) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS kettle_types (
        id SMALLSERIAL PRIMARY KEY,
        type_name VARCHAR(20) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS kettles (
        id BIGSERIAL PRIMARY KEY,
        model_code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(50) NOT NULL,
        producer_id BIGINT NOT NULL REFERENCES producers(id) ON DELETE RESTRICT,
        kettle_type_id SMALLINT REFERENCES kettle_types(id) ON DELETE RESTRICT,
        capacity NUMERIC(5,2),
        material_id SMALLINT REFERENCES materials(id) ON DELETE RESTRICT,
        color_id SMALLINT REFERENCES colors(id) ON DELETE RESTRICT,
        price NUMERIC(12,2),
        warranty_months INT,
        release_date DATE,
        icon BYTEA
    );
    """)

    conn.commit()
    conn.close()
    print("Tables checked/created.")


def init_db():
    create_database_if_not_exists()
    create_tables()
