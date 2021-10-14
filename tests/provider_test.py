''' Test to check providers '''
import unittest

from helpers.providers.http_provider import (GenericHTTPProvider,
                                             GitHubHTTPProvider,
                                             GitlabHTTPProvider)

# pylint: disable=protected-access


class GitHubHTTPProviderTests(unittest.TestCase):
    ''' GitHub Provider Tests '''

    def setUp(self):
        self.provider = GitHubHTTPProvider
        self.test_url = 'https://github.com/Bonial-International-GmbH/MkRadar/blob/main/README.md'

    def test_can_open(self):
        ''' Tests if provider check correctly if it can handle the url '''
        self.assertTrue(self.provider.can_open(self.test_url))
        self.assertFalse(self.provider.can_open(
            'github.com:Bonial-International-GmbH/MkRadar.git'))
        self.assertFalse(self.provider.can_open(
            'https://bitbucket.org/MysteryInc/MagicProject/src/master/'))

    def test_pre_url_modify(self):
        ''' Tests if the url are correctly re-writen '''
        self.assertEqual(
            self.provider._pre_url_modify(self.test_url),
            'https://raw.githubusercontent.com/Bonial-International-GmbH/MkRadar/main/README.md'
        )

    def test_unauthenticated(self):
        ''' Test if provider can download unauthenticated '''
        code = self.provider._get_page_unauthorized(self.test_url).status_code
        self.assertEqual(200, code)

    def test_authenticated(self):
        ''' Test if provider can download authenticated '''
        # Fixme: Don't know which repository to use

    def test_get_page(self):
        ''' Test if provider can download content '''
        content = self.provider.get_page(self.test_url)
        self.assertGreater(len(content), 0)


class GitLabHTTPProviderTests(unittest.TestCase):
    ''' GitLab Provider Tests '''

    def setUp(self):
        self.provider = GitlabHTTPProvider
        self.test_url = 'https://gitlab.com/Qrl/zabbix/-/blob/master/README.md'

    def test_can_open(self):
        ''' Tests if provider check correctly if it can handle the url '''
        self.assertTrue(self.provider.can_open(self.test_url))
        self.assertFalse(self.provider.can_open(
            'https://bitbucket.org/MysteryInc/MagicProject/src/master/'))

    def test_pre_url_modify(self):
        ''' Tests if the url are correctly re-writen '''
        self.assertEqual(
            self.provider._pre_url_modify(self.test_url),
            'https://gitlab.com/Qrl/zabbix/-/raw/master/README.md'
        )

    def test_unauthenticated(self):
        ''' Test if provider can download unauthenticated '''
        code = self.provider._get_page_unauthorized(self.test_url).status_code
        self.assertEqual(200, code)

    def test_authenticated(self):
        ''' Test if provider can download authenticated '''
        # Fixme: Don't know which repository to use

    def test_get_page(self):
        ''' Test if provider can download content '''
        content = self.provider.get_page(self.test_url)
        self.assertGreater(len(content), 0)


class GenericHTTPProviderTests(unittest.TestCase):
    ''' GitLab Provider Tests '''

    def setUp(self):
        self.provider = GenericHTTPProvider
        self.test_url = 'https://raw.githubusercontent.com/Bonial-International-GmbH/MkRadar/main/README.md'

    def test_can_open(self):
        ''' Tests if provider check correctly if it can handle the url '''
        self.assertTrue(self.provider.can_open(self.test_url))
        self.assertFalse(self.provider.can_open(
            'github.com:Bonial-International-GmbH/MkRadar.git'))

    def test_pre_url_modify(self):
        ''' Tests if the url are correctly re-writen '''
        self.assertEqual(
            self.provider._pre_url_modify(self.test_url),
            self.test_url
        )

    def test_unauthenticated(self):
        ''' Test if provider can download unauthenticated '''
        code = self.provider._get_page_unauthorized(self.test_url).status_code
        self.assertEqual(200, code)

    def test_authenticated(self):
        ''' Test if provider can NOT download authenticated '''
        self.assertRaises
        self.assertRaises(
            NotImplementedError,
            self.provider._get_page_authorized,
            self.test_url
        )

    def test_get_page(self):
        ''' Test if provider can download content '''
        content = self.provider.get_page(self.test_url)
        self.assertGreater(len(content), 0)
