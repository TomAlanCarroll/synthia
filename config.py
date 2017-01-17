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


_platform = platform.uname()[4]
path_to_file = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# filter warnings, load the configuration
warnings.filterwarnings("ignore")

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=False, help="path to the JSON configuration file")
args = vars(ap.parse_args())

CONFIG = json.loads(args["config"]);

def get(key):
    return CONFIG[key]