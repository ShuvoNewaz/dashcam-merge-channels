import os
import argparse
from utils import *

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
start_indices = {"front": args.front_start, "back": args.back_start,
               "left": args.left_start, "right": args.right_start}
end_indices = {"front": args.front_end, "back": args.back_end,
               "left": args.left_end, "right": args.right_end}
dirs = {"front": frontDir, "back": backDir,
        "left": leftDir, "right": rightDir}
names = {"front": frontNames, "back": backNames,
         "left": leftNames, "right": rightNames}
h = 720
w = h * 16 // 9

for channel in channels:
    start_index, end_index = start_indices[channel], end_indices[channel]
    # Cascade all videos of a single channel
    writeText(names[channel][start_index:end_index],
              dirs[channel], f"{channel}_{args.date}.txt")
    os.system(f"ffmpeg -y -f concat -safe 0 -i {channel}_{args.date}.txt \
                -c:v copy -an {channel}_temp.{ext}")
    
    # Delete the individual channel videos after cascading
    deleteFilesFromList(names[channel][start_index:end_index],
                        dirs[channel])
    os.system(f"rmdir {dirs[channel]}")
    
    video_length = get_video_duration(f"{channel}_temp.{ext}")
    if channel == "left":
        desired_length = video_length
    # Make all channel videos the same length as left channel (sync with driver)
    change_duration(f"{channel}_temp.{ext}",
                    f"{channel}_{args.date}.{ext}",
                    target_duration=desired_length)
    
    # Delete the .txt files and erroneous duration video after use
    os.system(f"rm {f"{channel}_{args.date}.txt"}")
    os.system(f"rm {f"{channel}_temp.{ext}"}")

# Stack videos
stack_videos(f"front_{args.date}.{ext}",
             f"back_{args.date}.{ext}",
             f"left_{args.date}.{ext}",
             f"right_{args.date}.{ext}",
             f"{args.date}.{ext}", w, h)

# Remove empty channel directories
for channel in channels:
    os.system(f"rm {f"{channel}_{args.date}.{ext}"}")