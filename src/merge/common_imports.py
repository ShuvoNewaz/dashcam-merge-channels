import os
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", type=str, required=True)
parser.add_argument("-ext", "--extension", type=str, default="ts")
args = parser.parse_args()

ext = args.extension
cwd = os.getcwd()
channels = ["left", "right", "front", "back"]