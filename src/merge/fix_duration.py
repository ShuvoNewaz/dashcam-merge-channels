from src.merge.common_imports import *
from src.utils.video_utils import *
from src.utils.common_utils import get_duration

desired_length = get_duration(f"{args.date}.wav")
for channel in channels:        
    # Make all channel videos the same length as left channel audio (sync with driver)
    change_duration(f"{channel}_{args.date}_temp.{ext}",
                    f"{channel}_{args.date}.{ext}",
                    target_duration=desired_length)
    
    # Delete the erroneous duration video after use
    os.system(f"rm {f"{channel}_{args.date}_temp.{ext}"}")