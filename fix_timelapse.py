import os
import argparse
import subprocess
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--indices_list", nargs='+',
                    action="append", type=int, required=True)
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

for indices, channel in zip(args.indices_list, channels):
    for i in range(len(indices)):
        file_name = f"{channel}/{names[channel][indices[i]]}"
        video_fps = get_fps(file_name)
        if video_fps < 24.5:
            convert_fps_with_duration_change(file_name,
                                             names[channel][indices[i]],
                                             25)
            os.system(f"mv {names[channel][indices[i]]} {file_name}")