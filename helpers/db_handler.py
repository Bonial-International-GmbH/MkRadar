"""Wrapper for all DB related stuff"""
import sqlite3
from os.path import join

from helpers.logger import Logger

from .config_handler import ConfigHandler
from .helper_datalcasses import MarkdownPage

logger = Logger.initial(__name__)


class DB:
    """check if URL was in the DB and content was not changed"""

    @staticmethod
    def connect_to_db():
        """ create a database connection to a database
        """
        try:
            sql_create_markdowns_table = """CREATE TABLE IF NOT EXISTS markdowns (
                                    id integer PRIMARY KEY,
                                    url text NOT NULL,
                                    markdown_file_path text NOT NULL,
                                    file_content_hash text NOT NULL,
                                    category text NOT NULL,
                                    title text NOT NULL,
                                    latest_update timestamp NOT NULL
                                );"""
            website_path = ConfigHandler.website_path
            conn = sqlite3.connect(join(website_path, "Mkradar.db"))
            # create projects table
            c = conn.cursor()
            c.execute(sql_create_markdowns_table)
            return conn
        except sqlite3.Error as e:
            logger.error(e)

    @staticmethod
    def get_all_markdowns() -> list[MarkdownPage]:
        ''' Returns all entries in database '''
        conn = DB.connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM markdowns ORDER BY category")
        data = cursor.fetchall()
        return [MarkdownPage(*entry) for entry in data]

    @staticmethod
    def is_there_any_new_update(now: str) -> int:
        conn = DB.connect_to_db()
        c = conn.cursor()
        c.execute("SELECT * FROM markdowns WHERE latest_update >=?", (now,))
        data = c.fetchall()
        return len(data)

    @staticmethod
    def insert_only_new_content(url: str, markdown_file_path: str, file_content_hash: str, category: str, title: str, now: str) -> bool:
        conn = DB.connect_to_db()
        c = conn.cursor()
        c.execute("SELECT file_content_hash FROM markdowns WHERE url=?", (url,))
        data = c.fetchall()
        conn.commit()
        if len(data) > 0:
            if file_content_hash == data[0][0]:
                return False
            else:
                c.execute(
                    "UPDATE markdowns SET file_content_hash=? WHERE url=?;", (file_content_hash, url))
                conn.commit()
                return True
        else:
            c.execute("INSERT INTO markdowns VALUES (null, ?, ?, ?, ?, ?, ?);",
                      (url, markdown_file_path, file_content_hash, category, title, now))
            conn.commit()
            return True

    @staticmethod
    def is_exist_in_db(markdown_file_path: str) -> bool:
        conn = DB.connect_to_db()
        c = conn.cursor()
        c.execute("SELECT * FROM markdowns WHERE markdown_file_path ==?",
                  (markdown_file_path,))
        data = c.fetchall()
        return bool(data)

    @staticmethod
    def get_all_markdown_file_paths() -> list:
        conn = DB.connect_to_db()
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        c.execute("SELECT markdown_file_path FROM markdowns")
        data = c.fetchall()
        return data

    @staticmethod
    def delete_markdown_via_filepath(markdown_file_path: str):
        conn = DB.connect_to_db()
        c = conn.cursor()
        c.execute("DELETE FROM markdowns WHERE markdown_file_path ==?;",
                  (markdown_file_path,))
        conn.commit()
