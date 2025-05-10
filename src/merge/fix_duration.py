from src.merge.common_imports import *

for channel in channels:
    video_length = get_video_duration(f"{channel}_{args.date}_temp.{ext}")
    if channel == "left":
        desired_length = video_length
    # Make all channel videos the same length as left channel (sync with driver)
    change_duration(f"{channel}_{args.date}_temp.{ext}",
                    f"{channel}_{args.date}.{ext}",
                    target_duration=desired_length)
    
    # Delete the .txt files and erroneous duration video after use
    os.system(f"rm {f"{channel}_{args.date}.txt"}")
    os.system(f"rm {f"{channel}_{args.date}_temp.{ext}"}")