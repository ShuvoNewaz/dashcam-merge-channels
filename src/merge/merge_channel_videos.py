from src.merge.common_imports import *
from src.utils.audio_utils import *
from src.utils.video_utils import *

frontDir = os.path.join(cwd, "Front")
backDir = os.path.join(cwd, "Back")
leftDir = os.path.join(cwd, "Left")
rightDir = os.path.join(cwd, "Right")

frontNames = os.listdir(frontDir)
backNames = os.listdir(backDir)
leftNames = os.listdir(leftDir)
rightNames = os.listdir(rightDir)
frontNames.sort()
backNames.sort()
leftNames.sort()
rightNames.sort()

mergedFileList = []

start_indices = {"front": args.front_start, "back": args.back_start,
               "left": args.left_start, "right": args.right_start}
end_indices = {"front": args.front_end, "back": args.back_end,
               "left": args.left_end, "right": args.right_end}
dirs = {"front": frontDir, "back": backDir,
        "left": leftDir, "right": rightDir}
names = {"front": frontNames, "back": backNames,
         "left": leftNames, "right": rightNames}

for channel in channels:
    start_index, end_index = start_indices[channel], end_indices[channel]
    if channel == "left":
        # Get audio
        audio_source_list = get_audio_source_list(names[channel][start_index:end_index],
                                                  dirs[channel])
        audio_file_list = build_audio_timeline(audio_source_list, args.date)

    # Cascade all videos of a single channel
    writeText(names[channel][start_index:end_index],
              dirs[channel], f"{channel}_{args.date}.txt")
    os.system(f"ffmpeg -y -f concat -safe 0 -i {channel}_{args.date}.txt \
                -c:v copy -an {channel}_{args.date}_temp.{ext}")
    os.system(f"rm {f"{channel}_{args.date}.txt"}")
    
    # Delete the individual channel videos after cascading
    deleteFilesFromList(names[channel][start_index:end_index],
                        dirs[channel])
    os.system(f"rmdir {dirs[channel]}")