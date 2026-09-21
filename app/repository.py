import os
import time
from contextlib import contextmanager
from typing import Any, Iterator

import psycopg
from psycopg.rows import dict_row


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:dev@localhost:5432/Flyrank",
)


@contextmanager
def get_connection() -> Iterator[psycopg.Connection[Any]]:
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection:
        yield connection


def initialize_database() -> None:
    for attempt in range(30):
        try:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS tasks (
                            id SERIAL PRIMARY KEY,
                            title TEXT NOT NULL,
                            done BOOLEAN NOT NULL DEFAULT FALSE
                        )
                        """
                    )

                    cursor.execute("SELECT COUNT(*) AS count FROM tasks")
                    count = cursor.fetchone()["count"]

                    if count == 0:
                        cursor.executemany(
                            """
                            INSERT INTO tasks (title, done)
                            VALUES (%s, %s)
                            """,
                            [
                                ("Learn Docker", False),
                                ("Connect PostgreSQL", False),
                                ("Build a task API", False),
                            ],
                        )

                connection.commit()
                return

        except psycopg.OperationalError:
            if attempt == 29:
                raise
            time.sleep(1)


def get_all_tasks() -> list[dict[str, Any]]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, done
                FROM tasks
                ORDER BY id
                """
            )
            return list(cursor.fetchall())


def get_task(task_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, done
                FROM tasks
                WHERE id = %s
                """,
                (task_id,),
            )
            return cursor.fetchone()


def create_task(title: str, done: bool) -> dict[str, Any]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING id, title, done
                """,
                (title, done),
            )
            task = cursor.fetchone()

        connection.commit()
        return task


def update_task(
    task_id: int,
    title: str,
    done: bool,
) -> dict[str, Any] | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET title = %s, done = %s
                WHERE id = %s
                RETURNING id, title, done
                """,
                (title, done, task_id),
            )
            task = cursor.fetchone()

        connection.commit()
        return task


def delete_task(task_id: int) -> bool:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s",
                (task_id,),
            )
            deleted = cursor.rowcount > 0

        connection.commit()
        return deleted