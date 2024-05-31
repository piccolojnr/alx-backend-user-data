#!/usr/bin/env python3
"""Filtered logger module"""

import re
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List, Tuple

PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values from the log"""
        og = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, og, self.SEPARATOR)


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str,
) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        pattern = rf"(?<={field}=).*?(?={separator}|$)"
        message = re.sub(pattern, redaction, message)
    return message


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object
    """
    logger = logging.Logger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logging.getLogger("user_data")


def get_db() -> MySQLConnection:
    """Get a database connection using credentials
    from environment variables.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    if not database:
        raise ValueError(
            "The database name must be set in\
                the environment variable PERSONAL_DATA_DB_NAME"
        )

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database,
    )


def main():
    """Main function"""
    logger = get_logger()

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = "; ".join(f"{key}={value}" for key, value in row.items())
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
