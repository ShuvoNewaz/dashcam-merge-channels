import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", type=str, required=True)
parser.add_argument("-i", "--indices", nargs='+', type=int, required=True)
args = parser.parse_args()

cwd = os.getcwd()
frontDir = os.path.join(cwd, "Front")
backDir = os.path.join(cwd, "Back")
leftDir = os.path.join(cwd, "Left")
rightDir = os.path.join(cwd, "Right")
mergedDir = os.path.join(cwd, f"Merged_{args.date}")
os.makedirs(mergedDir, exist_ok=True)

frontNames = os.listdir(frontDir)
backNames = os.listdir(backDir)
leftNames = os.listdir(leftDir)
rightNames = os.listdir(rightDir)
frontNames.sort()
backNames.sort()
leftNames.sort()
rightNames.sort()

def writeText(fileList, dir, name):
    with open(name, "w") as f:
        for fileName in fileList:
            fileName = os.path.join(dir, fileName)
            f.write(f"file {fileName} \n")
    f.close()

def deleteFilesFromList(fileList, dir):
    for fileName in fileList:
        fileName = os.path.join(dir, fileName)
        os.system(f"rm {fileName}")

mergedFileList = []

channels = ["front", "back", "left", "right"]
dirs = {"front": frontDir, "back": backDir, "left": leftDir, "right": rightDir}
names = {"front": frontNames, "back": backNames, "left": leftNames, "right": rightNames}

for i in range(len(args.indices) - 1):
    for channel in channels:
        # Merge video of separated times
        writeText(names[channel][args.indices[i]:args.indices[i + 1]], dirs[channel], f"{channel}_{i + 1}_{args.date}.txt")
        os.system(f"ffmpeg -f concat -safe 0 -i {channel}_{i + 1}_{args.date}.txt -c copy {channel}_{i + 1}_{args.date}.mp4")
        # Delete the .txt files after use
        os.system(f"rm {f"{channel}_{i + 1}_{args.date}.txt"}")
        # Delete the individual channel videos after fusing
        deleteFilesFromList(names[channel][args.indices[i]:args.indices[i + 1]], dirs[channel])

    # Stack videos
    os.system(f"ffmpeg -i front_{i + 1}_{args.date}.mp4 -i back_{i + 1}_{args.date}.mp4 \
              -i left_{i + 1}_{args.date}.mp4 -i right_{i + 1}_{args.date}.mp4 -filter_complex \"\
                [0:v]scale=960:540,setpts=PTS-STARTPTS[top_left]; \
                [1:v]scale=960:540,setpts=PTS-STARTPTS[top_right]; \
                [2:v]hflip,scale=960:540,setpts=PTS-STARTPTS[bottom_right]; \
                [3:v]hflip,scale=960:540,setpts=PTS-STARTPTS[bottom_left]; \
                [top_left][top_right]hstack=inputs=2[top]; \
                [bottom_left][bottom_right]hstack=inputs=2[bottom]; \
                [top][bottom]vstack=inputs=2[video] \" \
                -map \"[video]\" -map 2:a -shortest -video_track_timescale 12800 \
                -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 192k \
                ./Merged_{args.date}/{args.date}_{i + 1}.mp4")
    mergedFileList.append(f"{args.date}_{i + 1}.mp4")
    # Delete the channel individual files after use
    for channel in channels:
        os.system(f"rm {channel}_{i + 1}_{args.date}.mp4")
    
# Now merge the stacked videos
writeText(mergedFileList, os.path.join(cwd, f"Merged_{args.date}"), f"{args.date}.txt")
os.system(f"ffmpeg -f concat -safe 0 -i {args.date}.txt -c copy {args.date}.mp4")
# Delete the merge text file
os.system(f"rm {f"{args.date}.txt"}")
# Delete the individual merged videos
os.system(f"rm -r {mergedDir}")
# Delete empty folders
for channel in channels:
    os.system(f"rmdir {dirs[channel]}")