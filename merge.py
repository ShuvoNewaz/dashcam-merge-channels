import os
import argparse
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", type=str, required=True)
parser.add_argument("-s", "--start", type=int, required=True)
parser.add_argument("-e", "--end", type=int, required=True)
parser.add_argument("-ext", "--extension", type=str, default="ts")
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

mergedFileList = []

channels = ["left", "right", "front", "back"]
dirs = {"front": frontDir, "back": backDir,
        "left": leftDir, "right": rightDir}
names = {"front": frontNames, "back": backNames,
         "left": leftNames, "right": rightNames}
h = 720
w = h * 16 // 9

for channel in channels:
    # Merge video of separated times
    writeText(names[channel][args.start:args.end],
              dirs[channel], f"{channel}_{args.date}.txt")
    os.system(f"ffmpeg -y -f concat -safe 0 -i {channel}_{args.date}.txt \
                -c:v copy -an {channel}_temp.{ext}")
    
    # Delete the individual channel videos after fusing
    deleteFilesFromList(names[channel][args.start:args.end],
                        dirs[channel])
    os.system(f"rmdir {dirs[channel]}")
    
    video_length = get_video_duration(f"{channel}_temp.{ext}")
    if channel == "left":
        desired_length = video_length
    # Make all channel videos the same length
    change_duration(f"{channel}_temp.{ext}",
                    f"{channel}_{args.date}.{ext}",
                    target_duration=desired_length)
    
    # Delete the .txt files after use
    os.system(f"rm {f"{channel}_{args.date}.txt"}")
    os.system(f"rm {f"{channel}_temp.{ext}"}")

# Stack videos
stack_videos(f"front_{args.date}.{ext}",
             f"back_{args.date}.{ext}",
             f"left_{args.date}.{ext}",
             f"right_{args.date}.{ext}",
             f"{args.date}.{ext}", w, h)
for channel in channels:
    os.system(f"rm {f"{channel}_{args.date}.{ext}"}")