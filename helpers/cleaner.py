"""Clean dangling contents"""

from os import walk, remove
from os.path import join
from helpers.db_handler import DB
from helpers.logger import Logger

logger = Logger.initial(__name__)


class Cleaner:
    """Check if there was abandoned files which were not related to any entry in radar_config.yaml"""

    @staticmethod
    def db_cleaner():
        """
         This method will compare the number of entities in the radar_config.yaml and DB and clean DB
        """
        # TODO: Implement this
        logger.warn(f"This method still did not Implement")

    @staticmethod
    def abandon_markdown_cleaner():
        """
        This method will check markdownStorage folder and try to delete the abandon files
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
    def clean():
        """
        This method will cal all related methods
        """
        Cleaner.db_cleaner()
        Cleaner.abandon_markdown_cleaner()
