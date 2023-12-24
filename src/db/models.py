from src.db.di import get_db


def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT FALSE,
            is_superuser BOOLEAN NOT NULL DEFAULT FALSE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users(id)
        );
        """
    ]
    db_conn = get_db()

    with db_conn.cursor() as cursor:
        for command in commands:
            cursor.execute(command)
        db_conn.commit()
