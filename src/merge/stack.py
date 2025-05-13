from src.merge.common_imports import *
import os
from src.utils.video_utils import *

h = 720
w = h * 16 // 9
ext = args.extension

# Stack videos
stack_videos(f"front_{args.date}.{ext}",
             f"back_{args.date}.{ext}",
             f"left_{args.date}.{ext}",
             f"right_{args.date}.{ext}",
             f"{args.date}_no_audio.{ext}", w, h)
# Add audio
os.system(f"ffmpeg -y -i {args.date}_no_audio.{ext} -i {args.date}.wav \
          -c:v copy -c:a aac \
          -map 0:v:0 -map 1:a:0 \
          -shortest {args.date}.{ext}")
# Remove individual channel files
for channel in channels:
    os.system(f"rm {f"{channel}_{args.date}.{ext}"}")
os.system(f"rm {args.date}_no_audio.{ext} {args.date}.wav")
