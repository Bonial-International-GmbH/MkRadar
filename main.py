import yaml
from threading import Thread
from datetime import datetime
from helpers.compiler import Compiler
from helpers.logger import Logger

logger = Logger.initial(__name__)


def config_reader():

    with open("radar_config.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(exc)

    markdowns_in_config = []
    threads = []
    now = datetime.now()

    for item in config["wikiPages"]:
        logger.info(f"Registering {item['label']} thread")
        threads.append(Thread(target=Compiler.check_website_and_save_new_contents,
                              args=(item['url'], item['category'], item['label'], now)))

        markdowns_in_config.append(item)

    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        thread.join()

    Compiler.generate_new_static_html_site(now)


if __name__ == '__main__':
    logger.info("Starting the program")
    config_reader()
