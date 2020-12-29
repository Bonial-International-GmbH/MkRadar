"""Clean dangling contents"""

from os import walk, remove, path
from os.path import join
from helpers.db_handler import DB
from helpers.logger import Logger

logger = Logger.initial(__name__)


class Cleaner:
    """Check if there was abandoned files which were not related to any entry in radar_config.yaml"""

    @staticmethod
    def _db_cleaner(markdowns_in_config: list) -> bool:
        """
         What will happen if somebody delete an item in radar_config.yaml and re add it in the future?
         This method will compare the number of entities in the radar_config.yaml and DB and clean the DB
        """
        cleaned = False
        markdowns_in_db = DB.get_all_markdown_file_paths()
        for markdown_file_path in markdowns_in_db:
            if markdown_file_path not in markdowns_in_config:
                DB.delete_markdown_via_filepath(markdown_file_path)
                logger.info(f"This Mk record deleted from DB {markdown_file_path}")
                cleaned = True
        return cleaned

    @staticmethod
    def _abandon_markdown_cleaner():
        """
        This method will check markdownStorage folder and try to delete
        the abandon files which don't have any reference in the DB
        """
        existing_files_in_mds_path = [join(dir, file)
                                      for dir, sub, files in walk("website/docs")
                                      for file in files]
        del(existing_files_in_mds_path[0])
        for item in existing_files_in_mds_path:
            if not DB.is_exist_in_db(item):
                logger.info(f"This is going to be deleted: {item}")
                remove(item)

    @staticmethod
    def clean(markdowns_in_config: list) -> bool:
        """
        This method will cal all related methods
        """
        cleaned = Cleaner._db_cleaner(markdowns_in_config)
        Cleaner._abandon_markdown_cleaner()
        return cleaned
