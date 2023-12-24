from src.db.di import get_db


def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            email VARCHAR(256) UNIQUE NOT NULL,
            hashed_password VARCHAR(64) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE NOT NULL,
            is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW() NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS jwt_tokens (
            jti UUID PRIMARY KEY,
            is_blacklisted BOOLEAN DEFAULT FALSE NOT NULL,
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            device_id UUID NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS task_lists (
            id UUID PRIMARY KEY,
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(256) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT NOW() NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
        id UUID PRIMARY KEY,
        task_list_id UUID REFERENCES task_lists(id) ON DELETE CASCADE,
        title VARCHAR(256) NOT NULL,
        description TEXT,
        due_date TIMESTAMP,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT NOW() NOT NULL
        );
        """,
    ]
    db_conn = get_db()
    with db_conn.cursor() as cursor:
        for command in commands:
            cursor.execute(command)
        db_conn.commit()
