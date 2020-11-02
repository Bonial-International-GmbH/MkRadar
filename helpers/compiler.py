"""Save markdowns to the disks from the web"""
import hashlib
import yaml
import subprocess
from pathlib import Path
from helpers.providers import UrlOpener
from helpers.db_handler import DB
from helpers.logger import Logger
from helpers.cleaner import Cleaner

logger = Logger.initial(__name__)


class Compiler:
    """Will download MarkDown file and generate HTML from downloaded MDs"""

    @staticmethod
    def check_website_and_save_new_contents(url: str, category: str, label: str, now: str):

        file_name_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        markdown_directory_path = f"website/docs/{category}/"
        markdown_file_path = markdown_directory_path + file_name_hash + ".md"
        logger.info(f"Check Url: {url}")

        html = UrlOpener.open(url)
        url_content_hash = hashlib.md5(html.encode("utf-8")).hexdigest()
        logger.info(url_content_hash)

        # If something detect as a changed case from DB side we should save MD file to the disk and trigger HTML creator
        if DB.insert_only_new_content(url, markdown_file_path, url_content_hash, category, label, now):
            Path(markdown_directory_path).mkdir(parents=True, exist_ok=True)

            with open(markdown_file_path, "wb") as file:
                file.write(html.encode("utf-8"))
                logger.info(f"File was writen in {markdown_file_path}")

    @staticmethod
    def generate_new_menu():

        menu_items = {}
        db_menu_items = DB.get_markdowns_menu()
        for item in db_menu_items:
            title, file_address, category = item[0], item[1][13:], item[2]
            menu_items[category] = menu_items.get(category, [])
            menu_items[category].append({title: file_address})
        menu = {"site_name": "MkRadar", "nav": []}
        menu["nav"].append({"Home": "index.md"})
        for item in menu_items:
            menu["nav"].append({item: menu_items[item]})
        logger.info(f" Menu items: {menu}")

        with open("website/mkdocs.yml", 'w') as stream:
            stream.write(yaml.dump(menu))

    @staticmethod
    def generate_new_static_html_site(now: str):

        if DB.new_update(now):
            Compiler.generate_new_menu()

            p1 = subprocess.run(['mkdocs', 'build', '--clean'], capture_output=True, text=True, cwd='website')
            logger.info(p1.stdout)
            logger.error(p1.stderr)

            Cleaner.clean()
