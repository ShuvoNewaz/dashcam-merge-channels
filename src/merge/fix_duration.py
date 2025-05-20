from concurrent.futures import ThreadPoolExecutor, as_completed
from src.merge.common_imports import *
from src.utils.video_utils import *
from src.utils.common_utils import get_duration

desired_length = get_duration(f"{args.date}.wav")

def process_channel(channel):
    temp_file = f"{channel}_{args.date}_temp.{ext}"
    final_file = f"{channel}_{args.date}.{ext}"

    # Make channel video match desired length
    change_duration(temp_file, final_file, target_duration=desired_length)

    # Delete temp file
    os.remove(temp_file)

# Run all 4 channels in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_channel, channel) for channel in channels]
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error processing channel: {e}")