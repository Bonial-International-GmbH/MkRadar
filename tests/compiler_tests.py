#!/usr/bin/env python

import unittest
from pathlib import Path
from os.path import join
from helpers.compiler import Compiler


class CompilerTests(unittest.TestCase):
    website_path = "website"
    test_website_url = "https://github.com/Bonial-International-GmbH/MkRadar/blob/main/README.md"

    def test_get_all_mds_address_from_config_file(self):
        mds_list = Compiler._get_all_mds_address_from_config_file(self.website_path)
        self.assertIsInstance(mds_list, list)

    def test_generate_md_file_address(self):
        md_file_address = Compiler._generate_md_file_address(
            self.test_website_url,
            "OPS",
            "website")
        self.assertEqual(md_file_address, "website/docs/OPS/4b0ce8f7a2f18bda9c68d923291c59d3.md")

    def test_get_website_content(self):
        url_content_hash, html = Compiler._get_website_content(self.test_website_url, "public")
        self.assertIsNotNone(url_content_hash)
        self.assertIsNotNone(html)

    def test_write_into_file(self):
        file_name = "test.txt"
        Compiler._write_into_file(file_name, "This is a test", "wb")
        test_file = Path(file_name)
        self.assertTrue(test_file.is_file())

    def test_copy_index_md_to_docs(self):
        Compiler._copy_index_md_to_docs(self.website_path)
        test_file = Path(join(self.website_path, "docs", "index.md"))
        self.assertTrue(test_file.is_file())
