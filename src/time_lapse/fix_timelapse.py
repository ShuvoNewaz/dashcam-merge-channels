from src.utils.video_utils import *

def main():
    channels = ["front", "back", "left", "right"]
    time_lapses_list = get_time_lapse_videos(channels)
    fix_fps_from_dir_list(time_lapses_list)

if __name__ == "__main__":
    main()
