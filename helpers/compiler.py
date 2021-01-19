"""Save markdowns to the disks from the web"""
import hashlib
import yaml
import subprocess
from pathlib import Path
from helpers.providers import UrlOpener
from helpers.db_handler import DB
from helpers.logger import Logger
from helpers.cleaner import Cleaner
from helpers.aws_helper import AWS
from os.path import join, basename

logger = Logger.initial(__name__)


class Compiler:
    """Will download MarkDown file and generate static website from downloaded MDs if it is needed"""

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parent.parent

    @staticmethod
    def config_reader() -> list:
        config = []
        with open(join(Compiler.get_project_root(), "radar_config.yaml"), 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.error(exc)
        return config["wikiPages"]

    @staticmethod
    def _get_all_mds_address_from_config_file(website_path: str) -> list:
        return [Compiler._generate_md_file_address(md["url"], md["category"], website_path) for md in Compiler.config_reader()]

    @staticmethod
    def _generate_md_file_address(url: str, category: str, website_path: str) -> str:
        markdown_directory_path = join(website_path, "docs", category)
        Path(markdown_directory_path).mkdir(parents=True, exist_ok=True)
        file_name = hashlib.md5(url.encode("utf-8")).hexdigest() + ".md"
        markdown_file_path = join(markdown_directory_path, file_name)
        return markdown_file_path

    @staticmethod
    def _get_website_content(url: str, url_type: str) -> tuple:
        logger.info(f"Check Url: {url}")
        html = UrlOpener.open(url, url_type)
        url_content_hash = hashlib.md5(html.encode("utf-8")).hexdigest()
        logger.info(url_content_hash)
        return url_content_hash, html

    @staticmethod
    def _write_into_file(file: str, filecontent: str, writemode: str):
        with open(file, writemode) as file:
            if writemode == "wb":
                file.write(filecontent.encode("utf-8"))
            else:
                file.write(filecontent)
            logger.info(f"File was writen in {file}")

    @staticmethod
    def save_content_if_it_was_new(url: str, category: str, title: str, now: str, website_path: str, url_type: str = "public"):

        markdown_file_path = Compiler._generate_md_file_address(url, category, website_path)

        url_content_hash, url_content_html = Compiler._get_website_content(url, url_type)

        # If something detect as a changed case from DB side we should save MD file to the disk and trigger HTML creator
        if DB.insert_only_new_content(url, markdown_file_path, url_content_hash, category, title, now):
            Compiler._write_into_file(markdown_file_path, url_content_html, "wb")

    @staticmethod
    def _get_menu_items_from_db() -> dict:
        menu_items = {}
        db_menu_items = DB.get_markdowns_menu()
        for item in db_menu_items:
            title, file_address, category = item[0], basename(item[1]), item[2]
            menu_items[category] = menu_items.get(category, [])
            menu_items[category].append({title: category + "/" + file_address})
        return menu_items

    @staticmethod
    def _generate_new_mkdocs_config(website_path: str):
        menu_items = Compiler._get_menu_items_from_db()
        logger.info(f" Menu items: {menu_items}")
        mkdocs_config = {
            "site_name": "MkRadar",
            "site_dir": "html",
            "nav": []}
        mkdocs_config["nav"].append({"Home": "index.md"})
        for item in menu_items:
            mkdocs_config["nav"].append({item: menu_items[item]})

        Compiler._write_into_file(join(website_path, "mkdocs.yml"), yaml.dump(mkdocs_config), 'w')

    @staticmethod
    def _copy_index_md_to_docs(website_path: str):
        with open(join(Compiler.get_project_root(), 'index.md')) as file:
            Compiler._write_into_file(join(website_path, "docs", "index.md"), file.read(), 'w')
            Compiler._write_into_file(join(website_path, "docs", "index.md"), file.read(), 'w')

    @staticmethod
    def generate_new_static_html_site_if_it_is_needed(
            now: str, website_path: str, s3_bucket_name: str, s3_bucket_destination: str):
        config_file_change_detected = Cleaner.clean(
            Compiler._get_all_mds_address_from_config_file(website_path),
            website_path
        )
        any_new_item_in_the_db = DB.is_there_any_new_update(now)

        if config_file_change_detected or any_new_item_in_the_db:
            Compiler._generate_new_mkdocs_config(website_path)
            Compiler._copy_index_md_to_docs(website_path)
            p1 = subprocess.run(['mkdocs', 'build', '--clean'], capture_output=True, text=True, cwd=website_path)
            logger.info(p1.stdout)
            logger.error(p1.stderr)
            if s3_bucket_name:
                AWS.clean_s3_bucket(s3_bucket_name)
                AWS.copy_to_s3(website_path, s3_bucket_name, s3_bucket_destination)

