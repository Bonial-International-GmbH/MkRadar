import yaml
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from helpers.logger import Logger

logger = Logger.initial(__name__)

class ConfigHandler:
    """Takes care of the config file"""

    @staticmethod
    def validate(filename: str):
        """ Validates the provided radar_config """

        with open(filename,'r') as fh:
            config = yaml.safe_load(fh)
        with open('radar_config.schema.json', 'r') as fh:
            schema = json.load(fh)

        try:
            logger.debug("Validating config file")
            validate(instance=config, schema=schema)
        except:
            # Nicer error handling for the user would be nice
            logger.error("Soemthig is wrong with the config file")
            raise

    @staticmethod
    def get_mk_pages(filename: str) -> list:
        """Parses the config file and returns the markdown pages"""
        ConfigHandler.validate(filename)
        with open(filename,'r') as fh:
            config = yaml.safe_load(fh)
        return config["wikiPages"]
