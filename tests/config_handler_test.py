import unittest
import json
import tempfile
from helpers.config_handler import ConfigHandler
from jsonschema.exceptions import ValidationError

class ConfigHandlerTests(unittest.TestCase):

    def setUp(self):
        self.bad_config = {
            'version': '1',
            'wikiPages': [
                {  # Missing url
                    'title': 'aws-nuke',
                    'category': 'OPS',
                },
                {
                    'title': 'site24*7',
                    'category': 'OPS',
                    'type': 5,  # Should be string
                    'notification': False,
                    'tags': 'terraform, go, shell',
                    'url': 'https://github.com/Bonial-International-GmbH/terraform-provider-site24x7/blob/master/README.md'}
            ]
        }
        self.bad_config_file = tempfile.NamedTemporaryFile(mode='wt')
        self.bad_config_file.write(json.dumps(self.bad_config))

        ConfigHandler.radar_config = self.bad_config_file.name

    def test_validator(self):
        self.assertRaises(
            ValidationError, ConfigHandler._validate_radar_config)

    def tearDown(self):
        self.bad_config_file.close()
