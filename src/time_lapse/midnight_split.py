from src.utils.video_utils import *
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", type=str, required=True)
    args = parser.parse_args()

    channels = ["front", "back", "left", "right"]
    for channel in channels:
        channel_videos = [file for file in os.listdir(channel)
                          if args.date in file]
        channel_videos.sort()

        # Only the last video may cross midnight
        suspect_video = os.path.join(channel, channel_videos[-1])
        
        split_at_midnight(suspect_video)

if __name__ == "__main__":
    main()