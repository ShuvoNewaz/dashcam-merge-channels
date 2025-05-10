import os
import argparse
from src.utils import *

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", type=str, required=True)
parser.add_argument("-fs", "--front_start", type=int, required=True)
parser.add_argument("-fe", "--front_end", type=int, required=True)
parser.add_argument("-bs", "--back_start", type=int, required=True)
parser.add_argument("-be", "--back_end", type=int, required=True)
parser.add_argument("-ls", "--left_start", type=int, required=True)
parser.add_argument("-le", "--left_end", type=int, required=True)
parser.add_argument("-rs", "--right_start", type=int, required=True)
parser.add_argument("-re", "--right_end", type=int, required=True)
parser.add_argument("-ext", "--extension", type=str, default="ts")
args = parser.parse_args()

ext = args.extension
cwd = os.getcwd()
channels = ["left", "right", "front", "back"]