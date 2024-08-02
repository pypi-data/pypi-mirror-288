import toml
import logging
import optilibre.models as models


def parse_config_file(config_file_path):
    """
    Parse the config file to build and store configuration in a global_config object.
    @param config_file_path: path to optilibre.conf
    """
    logging.info("Parsing " + config_file_path)
    logging.debug("Any error will be fatal.")
    with open(config_file_path, 'r') as f:
        config = toml.load(f)

    global_config = models.GlobalConfig(**config)

    return global_config




