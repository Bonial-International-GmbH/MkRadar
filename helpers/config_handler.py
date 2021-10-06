from os import getenv
import argparse
import json
import yaml
from jsonschema import validate
from helpers.logger import Logger

logger = Logger.initial(__name__)

RADAR_CONFIG_SCHEMA_FILE = 'radar_config.schema.json'


class ConfigHandler:
    """Takes care of the config file
    cli params overwrite evironment vars
    """

    radar_config = None
    website_path = None

    s3_bucket_name = None
    s3_bucket_destination = None

    @classmethod
    def init(cls):
        """Initializes the config handler"""
        cls._read_environment_vars()
        cls._parse_cli_arguments()
        cls._validate_radar_config()

    @classmethod
    def _read_environment_vars(cls):
        cls.radar_config = getenv('RADAR_CONFIG', 'radar_config.yaml')
        cls.website_path = getenv('MK_RADAR_BUILD_PATH', 'website')

        cls.s3_bucket_name = getenv('S3_BUCKET_NAME')
        cls.s3_bucket_destination = getenv('S3_BUCKET_DESTINATION')

    @classmethod
    def _parse_cli_arguments(cls):
        parser = argparse.ArgumentParser(
            description='Creates HTML file from repos')
        parser.add_argument('--radar_config', default=cls.radar_config,
                            help='Radar config file (default: %(default)s)')
        parser.add_argument('--out-dir', default=cls.website_path,
                            help='Output directory (default: %(default)s)')
        parser.add_argument('--s3_bucket_name')
        parser.add_argument('--s3_bucket_destination')
        args = parser.parse_args()

        cls.radar_config = args.radar_config
        cls.website_path = args.out_dir
        cls.s3_bucket_name = args.s3_bucket_name
        cls.s3_bucket_destination = args.s3_bucket_destination

        logger.debug(args)

    @classmethod
    def _validate_radar_config(cls):
        """ Validates the provided radar_config """

        with open(cls.radar_config, 'r') as radar_config_fh:
            radar_config = yaml.safe_load(radar_config_fh)

        with open(RADAR_CONFIG_SCHEMA_FILE, 'r') as schema_fh:
            schema = json.load(schema_fh)

        try:
            logger.debug("Validating config file")
            validate(instance=radar_config, schema=schema)
        except Exception as error:
            # Nicer error handling for the user would be nice
            logger.error("Config error: %s", error)
            raise

    @classmethod
    def get_mk_pages(cls) -> list:
        """Parses the config file and returns the markdown pages"""
        with open(cls.radar_config, 'r') as radar_config:
            config = yaml.safe_load(radar_config)

        return config["wikiPages"]
