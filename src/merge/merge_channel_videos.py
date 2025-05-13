from src.merge.common_imports import *
from src.utils.audio_utils import *
from src.utils.video_utils import *

leftNames, rightNames, frontNames, backNames  = get_video_names(args.date, channels)

names = {"front": frontNames, "back": backNames,
         "left": leftNames, "right": rightNames}

for channel in channels:
    channel_dir = os.path.join(cwd, channel)
    if channel == "left":
        # Get audio
        audio_source_list = get_audio_source_list(names[channel],
                                                  channel_dir)
        audio_file_list = build_audio_timeline(audio_source_list, args.date)

    # Cascade all videos of a single channel
    writeText(names[channel],
              channel_dir, f"{channel}_{args.date}.txt")
    os.system(f"ffmpeg -y -f concat -safe 0 -i {channel}_{args.date}.txt \
                -c:v copy -an {channel}_{args.date}_temp.{ext}")
    os.system(f"rm {f"{channel}_{args.date}.txt"}")
    
    # Delete the individual channel videos after cascading
    deleteFilesFromList(names[channel],
                        channel_dir)
    os.system(f"rmdir {channel_dir}")