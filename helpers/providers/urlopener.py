"""Prepare correct settings to get the MarkDown files"""
import os
import git
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


class UrlOpener:
    """Handle authentication automatically if it's needed and get the content"""

    @staticmethod
    def open(desired_url: str, url_type: str):
        logger.info(f"Check Url: {desired_url}")
        for provider in PROVIDERS:
            if provider.can_open(desired_url):
                logger.debug(f"Using {provider} as provider for {desired_url}")
                return provider.get_page(desired_url)
