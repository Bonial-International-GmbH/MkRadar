"""Save markdowns to the disks from the web"""
import hashlib
import subprocess
from os.path import basename, join
from pathlib import Path

import yaml
from helpers.aws_helper import AWS
from helpers.cleaner import Cleaner
from helpers.config_handler import ConfigHandler
from helpers.db_handler import DB
from helpers.logger import Logger
from helpers.providers import UrlOpener

logger = Logger.initial(__name__)


class Compiler:
    """Will download MarkDown file and generate static website from downloaded MDs if it is needed"""

    @staticmethod
    def get_project_root() -> Path:
        ''' Retrieves base directory '''
        return Path(__file__).parent.parent

    @staticmethod
    def _get_all_mds_address_from_config_file(website_path: str) -> list[str]:
        ''' Returns a list of the hashes of the markdown files '''
        return [Compiler._generate_md_file_address(md["url"], md["category"], website_path) for md in ConfigHandler.get_mk_pages()]

    @staticmethod
    def _generate_md_file_address(url: str, category: str, website_path: str) -> str:
        ''' Create directory for the markdown file and returns hashed filenames '''
        markdown_directory_path = join(website_path, "docs", category)
        Path(markdown_directory_path).mkdir(parents=True, exist_ok=True)
        file_name = hashlib.md5(url.encode("utf-8")).hexdigest() + ".md"
        markdown_file_path = join(markdown_directory_path, file_name)
        return markdown_file_path

    @staticmethod
    def _get_website_content(url: str, url_type: str) -> tuple[str, str]:
        ''' Returns downloaded content and hash of the content '''
        logger.info("Check Url: %s", url)
        html = UrlOpener.open(url, url_type)
        url_content_hash = hashlib.md5(html.encode("utf-8")).hexdigest()
        logger.info(url_content_hash)
        return url_content_hash, html

    @staticmethod
    def _write_into_file(file: str, filecontent: str, writemode: str):
        ''' writes content into file '''
        with open(file, writemode) as output_file:
            if writemode == "wb":
                output_file.write(filecontent.encode("utf-8"))
            else:
                output_file.write(filecontent)
            logger.info("File was writen in %s", file)

    @staticmethod
    def save_content_if_it_was_new(url: str, category: str, title: str, now: str, website_path: str, url_type: str = "public"):
        ''' Check content against database and if new writes new file '''
        markdown_file_path = Compiler._generate_md_file_address(
            url, category, website_path)

        url_content_hash, url_content_html = Compiler._get_website_content(
            url, url_type)

        # If something detect as a changed case from DB side we should save MD file to the disk and trigger HTML creator
        if DB.insert_only_new_content(url, markdown_file_path, url_content_hash, category, title, now):
            Compiler._write_into_file(
                markdown_file_path, url_content_html, "wb")

    @staticmethod
    def _get_menu_items_from_db() -> dict:
        ''' Return a dict with all mardown items in database '''
        menu_items: dict = {}
        db_menu_items = DB.get_markdowns_menu()
        for item in db_menu_items:
            title, file_address, category = item[0], basename(item[1]), item[2]
            menu_items[category] = menu_items.get(category, [])
            menu_items[category].append({title: category + "/" + file_address})
        menu_items = dict(sorted(menu_items.items()))
        return menu_items

    @staticmethod
    def _generate_new_mkdocs_config(website_path: str):
        menu_items = Compiler._get_menu_items_from_db()
        logger.info(" Menu items: %s", menu_items)
        mkdocs_config = {
            "site_name": "MkRadar",
            "site_dir": "html",
            "use_directory_urls": False,
            "theme": {
                "name": "material"},
            "nav": []}
        mkdocs_config["nav"].append({"Home": "index.md"})
        for item in menu_items:
            mkdocs_config["nav"].append({item: menu_items[item]})

        Compiler._write_into_file(
            join(website_path, "mkdocs.yml"), yaml.dump(mkdocs_config), 'w')

    @staticmethod
    def _copy_index_md_to_docs(website_path: str):
        with open(join(Compiler.get_project_root(), 'index.md')) as file:
            Compiler._write_into_file(
                join(website_path, "docs", "index.md"), file.read(), 'w')

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
            mkdocs_process = subprocess.run(['mkdocs', 'build', '--clean'],
                                            capture_output=True, text=True, cwd=website_path)
            logger.info(mkdocs_process.stdout)
            logger.error(mkdocs_process.stderr)
            if s3_bucket_name:
                AWS.clean_s3_bucket(s3_bucket_name)
                AWS.copy_to_s3(website_path, s3_bucket_name,
                               s3_bucket_destination)
