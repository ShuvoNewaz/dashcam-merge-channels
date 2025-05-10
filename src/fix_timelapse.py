import os
import argparse
from src.utils import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--indices_list", nargs='+',
                    action="append", type=int, required=False)
parser.add_argument("-s", "--slices_list", nargs='+',
                    action="append", type=int, required=False)
parser.add_argument("-c", "--channels",
                    action="append", type=str, required=True)
parser.add_argument("-e", "--extension", type=str, default="ts")
args = parser.parse_args()

ext = args.extension
cwd = os.getcwd()
frontDir = os.path.join(cwd, "Front")
backDir = os.path.join(cwd, "Back")
leftDir = os.path.join(cwd, "Left")
rightDir = os.path.join(cwd, "Right")

frontNames = os.listdir(frontDir)
backNames = os.listdir(backDir)
leftNames = os.listdir(leftDir)
rightNames = os.listdir(rightDir)
frontNames.sort()
backNames.sort()
leftNames.sort()
rightNames.sort()

channels = args.channels
dirs = {"Front": frontDir, "Back": backDir,
        "Left": leftDir, "Right": rightDir}
names = {"Front": frontNames, "Back": backNames,
         "Left": leftNames, "Right": rightNames}


# Disjoint indices
if args.indices_list is not None:
    fix_fps_from_idx_list(args.indices_list, channels, names)

# Slice indices. Useful when too many consecutive videos are time lapsed.
if args.slices_list is not None:
    for slices, channel in zip(args.slices_list, channels):
        for j in range(0, len(slices) - 1, 2):
            indices_list = list(range(args.slices_list[j],
                                    args.slices_list[j + 1]))
            fix_fps_from_idx_list(indices_list, channels, names)