import shutil
import os
import argparse
from datetime import datetime, timedelta
from src.utils.video_utils import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", type=str, required=True)
    parser.add_argument("-sd", "--sd_card_dir", type=str, required=True)
    parser.add_argument("-ext", "--extension", type=str, default="ts")
    args = parser.parse_args()

    dashCamHome = args.sd_card_dir
    date = args.date
    ext = args.extension

    dst_folders = ["front", "back", "right", 'left']
    src_folders = ["F", "R", "FR", "FL"]

    for subDir in ["video", "park", 'event']:
        for src_subDir, dst_dir in zip(src_folders, dst_folders):
            print(f"Copying {dst_dir} channel files from {subDir}...")
            os.makedirs(dst_dir, exist_ok=True)
            src_dir = os.path.join(dashCamHome, subDir, src_subDir)
            file_list = os.listdir(src_dir)
            file_list.sort()
            for file in file_list:
                src_file_dir = os.path.join(src_dir, file)
                if date in file and ext in file:
                    end_time_str = get_modification_time_from_exif(src_file_dir)
                    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                    duration_sec = get_duration(src_file_dir)
                    fps = get_fps(src_file_dir)
                    if has_audio(src_file_dir):
                        fps = 1 # To avoid duration issues with non-timelapse videos
                    start_time = end_time - timedelta(seconds=duration_sec*fps)

                    # Copy the files and rename them to correct start times
                    dst_filename = start_time.strftime(f"%Y%m%d_%H%M%S{src_subDir}.{ext}")
                    dst_file_dir = os.path.join(dst_dir, dst_filename)
                    shutil.copy(src_file_dir, dst_file_dir)

if __name__ == "__main__":
    main()