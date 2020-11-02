"""Prepare correct settings to get the MarkDown files"""
import requests
from helpers.logger import Logger

logger = Logger.initial(__name__)


class UrlOpener:
    """Handle authentication automatically if it's needed and get the content"""

    @staticmethod
    def open(desired_url):
        logger.info(f"Check Url: {desired_url}")
        url_getter = UrlOpener._detect(desired_url)
        return UrlOpener.download_website(url_getter)

    @staticmethod
    def _detect(desired_url):
        if "bitbucket.org" in desired_url:
            return UrlOpener._bitbucket(desired_url)
        else:
            return requests.get(desired_url)

    @staticmethod
    def download_website(url_getter):
        with url_getter as response:
            html = response.text
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                logger.error(f"Http Error:{err}")
                raise SystemExit(err)
            except requests.exceptions.ConnectionError as err:
                logger.error(f"Error Connecting:{err}")
                raise SystemExit(err)
            except requests.exceptions.Timeout as err:
                logger.error(f"Timeout Error:{err}")
                raise SystemExit(err)
            except requests.exceptions.RequestException as err:
                logger.error(f"Some Error happened:{err}")
                raise SystemExit(err)
            return html

    @staticmethod
    def _bitbucket(url):
        url = url.replace("bitbucket.org/", "api.bitbucket.org/2.0/repositories/")
        return requests.get(url, auth=("USERNAME", "APP_PASSWORD"))
