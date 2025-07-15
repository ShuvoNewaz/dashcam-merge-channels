from src.merge.common_imports import *
import os
from src.utils.video_utils import *
from src.utils.common_utils import removeFile


def main():
    h = 720
    w = h * 16 // 9
    ext = args.extension

    # Stack videos
    stack_videos(f"front_{args.date}.{ext}",
                f"back_{args.date}.{ext}",
                f"left_{args.date}.{ext}",
                f"right_{args.date}.{ext}",
                f"{args.date}_no_audio.{ext}", w, h)

    # Remove individual channel files
    for channel in channels:
        removeFile(f"{channel}_{args.date}.{ext}")

    # Add audio
    subprocess.run(["ffmpeg", "-y",
                    "-i", f"{args.date}_no_audio.{ext}",
                    "-i", f"{args.date}.wav",
                    "-c:v", "copy", "-c:a", "aac",
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-shortest", f"{args.date}.{ext}"])

    # Remove the silent video and the audio files
    for file in [f"{args.date}_no_audio.{ext}", f"{args.date}.wav"]:
        removeFile(file)

if __name__ == "__main__":
    main()