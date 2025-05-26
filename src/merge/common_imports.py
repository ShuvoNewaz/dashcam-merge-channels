import os
import argparse
import subprocess
from src.utils.common_utils import parseBool

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", type=str, required=True)
parser.add_argument("-ext", "--extension", type=str, default="ts")
parser.add_argument("-p", "--parallel", type=str, default="True")
args = parser.parse_args()

ext = args.extension
parallel = parseBool(args.parallel)

cwd = os.getcwd()
channels = ["left", "right", "front", "back"]