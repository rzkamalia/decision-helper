import datetime
import json
import time
from contextlib import contextmanager

import psycopg2

from src import app_config


@contextmanager
def get_db_connection():
    """Connecting to database."""
    conn = psycopg2.connect(app_config.database_url)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_tables_if_not_exists(retries: int = 3, delay: int = 2):
    """Create tables if they don't exist."""
    for attempt in range(retries):

        try:
            with get_db_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS question_logs (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP NOT NULL,
                        context TEXT,
                        options JSONB,
                        questions JSONB,
                        image_content JSONB,
                        web_search_content TEXT
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS decision_logs (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) NOT NULL,
                        chosen_option TEXT,
                        reason TEXT,
                        question_answer_pairs JSONB,
                        created_at TIMESTAMP NOT NULL
                    )
                    """
                )
            print("Tables created successfully.")
        except Exception as e:
            if attempt < retries - 1:
                print(f"DB not ready, retrying in {delay}s...")
                time.sleep(delay)
            else:
                print("Error creating tables:", e)
                raise


def save_question_log(  # noqa: PLR0913
    user_id: str,
    context: str,
    options: list[str],
    questions: list[str],
    image_content: str,
    web_search_content: str,
):
    """Save generate question log to database."""
    try:
        created_at = datetime.datetime.now().replace(microsecond=0).isoformat()

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO question_logs (user_id, created_at, context, options, questions, image_content, web_search_content)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,  # noqa: E501
                (
                    user_id,
                    created_at,
                    context,
                    json.dumps(options),
                    json.dumps(questions),
                    json.dumps(image_content),
                    web_search_content,
                ),
            )
            print("Insert to question_logs successful")
    except Exception as e:
        print("Error during save_question_log:", e)
        raise


def save_decision_log(user_id: str, chosen_option: str, question_answer_pairs: list[dict[str, str]], reason: str):
    """Save generate decision log to database."""

    try:
        created_at = datetime.datetime.now().replace(microsecond=0).isoformat()

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO decision_logs (user_id, chosen_option, reason, question_answer_pairs, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    chosen_option,
                    reason,
                    json.dumps(question_answer_pairs),
                    created_at,
                ),
            )
            print("Insert to decision_logs successful")
    except Exception as e:
        print("Error during save_decision_log:", e)
        raise


def get_question_log(user_id: str) -> dict:
    """Query latest question_log by user_id."""
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT context, options, image_content, web_search_content
                FROM question_logs
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                return {
                    "context": row[0],
                    "options": row[1],
                    "image_content": row[2],
                    "web_search_content": row[3],
                }
            else:
                raise ValueError(f"No question log found for user_id {user_id}")
    except Exception as e:
        print("Error during get_question_log:", e)
        raise
