"""Prepare correct settings to get the MarkDown files"""
import os
import tempfile
from helpers.logger import Logger
from .HTTPProvider import GitHubHTTPProvider, GitlabHTTPProvider, BitBucketHTTPProvider, GenericHTTPProvider

logger = Logger.initial(__name__)


PROVIDERS = [
    GitHubHTTPProvider,
    GitlabHTTPProvider,
    BitBucketHTTPProvider,
    GenericHTTPProvider
]


class NoProviderFoundException(Exception):

    def __init__(self, url, message):
        self.url = url
        self.message = message
        super().__init__(self.message)


class UrlOpener:
    """Handle authentication automatically if it's needed and get the content"""

    @staticmethod
    def open(desired_url: str, url_type: str):
        logger.info(f"Check Url: {desired_url}")

        capable_provider = [
            provider for provider in PROVIDERS if provider.can_open(desired_url)]
        if [] == capable_provider:
            msg = f"No capable provider found for {desired_url}"
            logger.error(msg)
            raise NoProviderFoundException(desired_url, msg)

        provider = capable_provider[0]  # Take first capable provider
        logger.debug(f"Using {provider} as provider for {desired_url}")
        return provider.get_page(desired_url)
