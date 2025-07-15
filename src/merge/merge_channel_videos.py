from src.merge.common_imports import *
from src.utils.audio_utils import *
from src.utils.video_utils import *
from src.utils.common_utils import removeFile
from concurrent.futures import ThreadPoolExecutor, as_completed


def mergeChannelVideos(channel):
    channel_dir = os.path.join(cwd, channel)

    # Cascade all videos of a single channel
    writeText(names[channel],
              channel_dir, f"{channel}_{args.date}.txt")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                    "-i", f"{channel}_{args.date}.txt",
                    "-c:v", "copy", "-an",
                    f"{channel}_{args.date}_temp.{ext}"])
    removeFile(f"{channel}_{args.date}.txt")
    
    # Delete the individual channel videos after cascading
    deleteFilesFromList(names[channel],
                        channel_dir)
    if os.path.isdir(channel_dir) and not os.listdir(channel_dir):
        os.rmdir(channel_dir)

def main():
    global names
    leftNames, rightNames, frontNames, backNames  = get_video_names(args.date, channels)
    names = {"front": frontNames, "back": backNames,
            "left": leftNames, "right": rightNames}

    # Get audio
    audio_source_list = get_audio_source_list(leftNames,
                                            os.path.join(cwd, "left"))
    audio_file_list = build_audio_timeline(audio_source_list, args.date)

    if parallel:
        # Run all 4 channels in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(mergeChannelVideos, channel) for channel in channels]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing channel: {e}")
    else:
        for channel in channels:
            mergeChannelVideos(channel)

if __name__ == "__main__":
    main()