from src.utils.video_utils import *
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", type=str, required=True)
parser.add_argument("-sd", "--sd_card_dir", type=str, required=True)
args = parser.parse_args()

channels = ["front", "back", "left", "right"]
for channel in channels:
    channel_videos = [file for file in os.listdir(channel)
                         if args.date in file]
    channel_videos.sort()
    suspect_video = os.path.join(channel, channel_videos[-1])
    
    # Only check if time lapse crosses midnight.
    # Regular videos don't make much of a difference
    if not has_audio(suspect_video):
        split_at_midnight(suspect_video, args.sd_card_dir)