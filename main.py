from threading import Thread
from datetime import datetime
from helpers.compiler import Compiler
from helpers.logger import Logger
from helpers.aws_helper import AWS
from helpers.config_handler import ConfigHandler

logger = Logger.initial(__name__)


def main():
    ConfigHandler.init()

    markdowns_in_config = []
    threads = []
    now = datetime.now()


    if ConfigHandler.s3_bucket_name:
        logger.info("Trying to use AWS S3")
        AWS.download_mkradar(
            s3_bucket_name,
            s3_bucket_destination,
            website_path
        )

    for item in ConfigHandler.get_mk_pages():
        logger.info(f"Registering {item['title']} thread")
        url_type = item.get('type', 'public')

        threads.append(
            Thread(
                target=Compiler.save_content_if_it_was_new,
                args=(item['url'], item['category'], item['title'], now, ConfigHandler.website_path, url_type)
            )
        )

        markdowns_in_config.append(item)

    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        thread.join()

    Compiler.generate_new_static_html_site_if_it_is_needed(now, ConfigHandler.website_path, ConfigHandler.s3_bucket_name, ConfigHandler.s3_bucket_destination)


if __name__ == '__main__':
    logger.info("Starting the program")
    main()
