import json
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text


def update_dev_logs(records: dict):
    try:
        connection_str = _get_connection_string()
        engine = create_engine(connection_str)
        with engine.begin() as connection:
            sql = """
            UPDATE dropbase_dev_logs
            SET
                context = :context,
                store_out = :store,
                stdout = :stdout,
                traceback = :traceback,
                message = :message,
                type = :type,
                completed_at = :completed_at
            WHERE id = :id;
            """  # noqa
            connection.execute(text(sql), records)
    except SQLAlchemyError as e:
        print(f"Failed to execute log record query: {e}")
        raise e
    finally:
        engine.dispose()


def _get_connection_string():
    dev_db = os.getenv("dev_db")
    if dev_db and isinstance(dev_db, str):
        dev_db = json.loads(dev_db)
        if dev_db.get("type") == "postgres":
            return f"postgresql://{dev_db['username']}:{dev_db['password']}@{dev_db['host']}:{dev_db['port']}/{dev_db['database']}"  # noqa
        elif dev_db.get("type") == "sqlite":
            return f"sqlite:///{dev_db['host']}"
        else:
            raise ValueError("Invalid database type")
    else:
        return "sqlite:///files/dev.db"
