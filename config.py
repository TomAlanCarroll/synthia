"""
    Configuration Loader
"""
import argparse
import warnings
import inspect
import os
import json
import sys
import platform

def to_node(type, message):
    print(json.dumps({type: message}))
    sys.stdout.flush()

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=False,
      help="Optional path to the JSON configuration file; Default is config.json")
args = vars(ap.parse_args())

# Filter warnings, load the configuration
warnings.filterwarnings("ignore")
if args["config"]:
    CONFIG = json.load(open(args["config"]))
else:
    # Default to conf.json
    CONFIG = json.load(open("config.json"))

def get(key):
    return CONFIG[key]