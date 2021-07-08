import unittest
from helpers.config_handler import ConfigHandler
from jsonschema.exceptions import ValidationError

class ConfigHandlerTests(unittest.TestCase):

    def setUp(self):
        self.bad_config = {
            'version': '1',
            'wikiPages': [
                {   #Missing url
                    'title': 'aws-nuke',
                    'category': 'OPS',
                },
                {
                    'title': 'site24*7',
                    'category': 'OPS',
                    'type': 5, #Should be string
                    'notification': False,
                    'tags': 'terraform, go, shell',
                    'url': 'https://github.com/Bonial-International-GmbH/terraform-provider-site24x7/blob/master/README.md'}
                ]
            }

    def test_validator(self):
        self.assertRaises(ValidationError, ConfigHandler.validate, self.bad_config)
        self.bad_config['wikiPages'][0]['url'] = "https://github.com/rebuy-de/aws-nuke/blob/master/README.md"
        self.assertRaises(ValidationError, ConfigHandler.validate, self.bad_config)



    def tearDown(self):
        pass
