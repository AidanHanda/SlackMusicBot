import argparse

import yaml

import main


def parse_config(file):
    """
    Checks the config values and brings them in
    :param file: The config.yml file
    :return: 
    """
    yaml_file = yaml.load(open(file))
    main.run(yaml_file)

pathToConfig = "./config.yml"
parser = argparse.ArgumentParser(description='Start the slack bot')
parser.add_argument('filepath', metavar='f')
args = parser.parse_args()
parse_config(args.filepath)
