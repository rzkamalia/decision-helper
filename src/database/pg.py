import datetime
import json
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


def save_question_log(  # noqa: PLR0913
    user_id: str,
    context: str,
    options: list[str],
    questions: list[str],
    image_content: str,
    web_search_content: str,
):
    """Save generate question log to database."""
    created_at = datetime.datetime.now().replace(microsecond=0).isoformat()

    try:
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
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO decision_logs (user_id, chosen_option, reason, question_answer_pairs)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_id,
                    chosen_option,
                    reason,
                    json.dumps(question_answer_pairs),
                ),
            )
            print("Insert to decision_logs successful")
    except Exception as e:
        print("Error during save_question_log:", e)
        raise
