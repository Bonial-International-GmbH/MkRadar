"""Prepare correct settings to get the MarkDown files"""
import requests
import os
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
        if "github.com" in desired_url:
            return UrlOpener._github(desired_url)
        elif "bitbucket.org" in desired_url:
            return UrlOpener._bitbucket(desired_url)
        elif "gitlab.com" in desired_url:
            return UrlOpener._gitlab(desired_url)
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
    def _github(url: str, mode: str = "private"):
        url = url.replace("/blob/", "/")
        url = url.replace("/raw/", "/")
        url = url.replace("github.com/", "raw.githubusercontent.com/")

        if mode == "public":
            return requests.get(url)
        else:
            token = os.getenv('GITHUB_TOKEN', '...')
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3.raw'}
            return requests.get(url, headers=headers)

    @staticmethod
    def _bitbucket(url: str, mode: str = "private"):
        url = url.replace("bitbucket.org/", "api.bitbucket.org/2.0/repositories/")
        if mode == "public":
            return requests.get(url)
        else:
            username = os.getenv('BITBUCKET_USERNAME', '...')
            password = os.getenv('BITBUCKET_APP_PASSWORD', '...')
            return requests.get(url, auth=(username, password))

    @staticmethod
    def _gitlab(url: str, mode: str = "private"):
        url = url.replace("gitlab.com/", "gitlab.com/api/v4/")
        # todo: complete the private section with help of below link
        # https://docs.gitlab.com/ee/api/repository_files.html#get-raw-file-from-repository
        if mode == "public":
            return requests.get(url)
        else:
            token = os.getenv('GITLAB_TOKEN', '...')
            headers = {'PRIVATE-TOKEN': token}
            return requests.get(url, headers=headers)

