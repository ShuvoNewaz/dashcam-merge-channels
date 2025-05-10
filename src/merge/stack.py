from src.utils import stack_videos
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", type=str, required=True)
parser.add_argument("-ext", "--extension", type=str, default="ts")
args = parser.parse_args()

h = 720
w = h * 16 // 9
ext = args.extension
channels = ["left", "right", "front", "back"]

# Stack videos
stack_videos(f"front_{args.date}.{ext}",
             f"back_{args.date}.{ext}",
             f"left_{args.date}.{ext}",
             f"right_{args.date}.{ext}",
             f"{args.date}.{ext}", w, h)

# # Remove individual channel files
# for channel in channels:
#     os.system(f"rm {f"{channel}_{args.date}.{ext}"}")