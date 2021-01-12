from os import getenv
from os.path import join
from threading import Thread
from datetime import datetime
from helpers.compiler import Compiler
from helpers.logger import Logger
from helpers.aws_helper import AWS

logger = Logger.initial(__name__)


def initial():

    config = Compiler.config_reader()

    markdowns_in_config = []
    threads = []
    now = datetime.now()

    website_path = getenv('MK_RADAR_BUILD_PATH', 'website')
    s3_bucket_name = getenv('S3_BUCKET_NAME', '')
    s3_bucket_destination = getenv('S3_BUCKET_DESTINATION', '')

    if s3_bucket_name and s3_bucket_destination:
        bn = s3_bucket_name
        bd = join(s3_bucket_destination, "Mkradar.db")
        fn = join(website_path, "Mkradar.db")
        logger.info(f"Downloading {bd} from {bn} to {fn}")
        AWS.download_from_s3(bn, bd, fn)

    for item in config:
        logger.info(f"Registering {item['title']} thread")
        url_type = item.get('type', 'public')

        threads.append(Thread(target=Compiler.save_content_if_it_was_new,
                              args=(item['url'], item['category'], item['title'], now, website_path, url_type)))

        markdowns_in_config.append(item)

    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        thread.join()

    Compiler.generate_new_static_html_site_if_it_is_needed(now, website_path, s3_bucket_name, s3_bucket_destination)


if __name__ == '__main__':
    logger.info("Starting the program")
    initial()
