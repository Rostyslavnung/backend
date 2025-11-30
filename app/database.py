import psycopg2
from flask import current_app

def get_connection(dbname=None):
    config = current_app.config

    return psycopg2.connect(
        database=dbname or config["DB_NAME"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        host=config["DB_HOST"],
        port=config["DB_PORT"],
    )

def create_database_if_not_exists():
    conn = get_connection("defaultdb")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (current_app.config["DB_NAME"],))
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {current_app.config['DB_NAME']}")
        print(f"Database '{current_app.config['DB_NAME']}' created.")

    conn.close()


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS producers (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS colors (
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR(30) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR(30) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS kettle_types (
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR(20) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS kettles (
        id BIGSERIAL PRIMARY KEY,
        model_code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(50) NOT NULL,
        producer_id BIGINT NOT NULL REFERENCES producers(id) ON DELETE RESTRICT,
        kettle_type_id SMALLINT REFERENCES kettle_types(id) ON DELETE RESTRICT,
        material_id SMALLINT REFERENCES materials(id) ON DELETE RESTRICT,
        color_id SMALLINT REFERENCES colors(id) ON DELETE RESTRICT,
        capacity NUMERIC(5,2),
        warranty_months INT,
        price NUMERIC(12,2),
        release_date DATE,
        icon BYTEA
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE
    );
    """)

    conn.commit()
    conn.close()
    print("Tables checked/created.")

def create_default_admin():
    from app.src.User import User, create_user
    if not User.get_by_username("admin"):
        create_user("admin", "admin123", is_admin=True)


def init_db():
    from flask import current_app
    with current_app.app_context():
        create_database_if_not_exists()
        create_tables()
        create_default_admin()