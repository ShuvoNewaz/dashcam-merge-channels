import os
import argparse
from src.utils.video_utils import *
from src.utils.audio_utils import has_audio

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--indices_list", nargs='+',
                    action="append", type=int, required=False)
parser.add_argument("-c", "--channels",
                    action="append", type=str, required=True)
args = parser.parse_args()

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

fix_fps_from_idx_list(args.indices_list, channels, names)