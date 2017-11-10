import os
import argparse
import yaml
import main

def parse_config(file):
    yaml_file = yaml.load(open(file))
    main.run(yaml_file)

os.system("pip install -r requirements.txt")
pathToConfig = "./config.yml"
parser = argparse.ArgumentParser(description='Start the slack bot')
parser.add_argument('filepath', metavar='f')
args = parser.parse_args()
parse_config(args.filepath)
