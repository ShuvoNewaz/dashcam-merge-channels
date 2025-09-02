from src.utils.video_utils import delayVideo
from src.utils.audio_utils import delayAudio
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", type=str, required=True)
    parser.add_argument("-ext", "--extension", type=str, default="ts")
    parser.add_argument("-t", "--type", type=str, required=True)
    parser.add_argument("-a", "--amount", type=str, required=True)
    args = parser.parse_args()

    assert args.type in ["video", "audio"], \
        "Type must be 'video' or 'audio'."

    file = f"{args.date}.{args.extension}"
    if args.type == "video":
        delayVideo(file, args.amount)
    else:
        delayAudio(file, args.amount)

if __name__ == "__main__":
    main()