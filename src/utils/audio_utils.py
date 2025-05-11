import os
import subprocess
from pathlib import Path
import shutil
from src.utils.common_utils import get_duration


def get_audio_source_list(fileList, dir):
    audio_source_list = []
    for fileName in fileList:
        fileName = os.path.join(dir, fileName)
        audio_source_list.append(fileName)

    return audio_source_list


def has_audio(file_path):
    """Check if a video file has an audio stream."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index", "-of", "csv=p=0", file_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return bool(result.stdout.strip())

def extract_audio(input_file, output_file):
    cmd = ['ffmpeg', '-y', '-i', input_file, '-vn',
           '-ar', '48000', '-ac', '2',
           '-acodec', 'pcm_s16le', output_file]
    subprocess.run(cmd, check=True)

def create_silence(duration, output_file):
    cmd = ['ffmpeg', '-y', '-f', 'lavfi',
           '-i', 'anullsrc=r=48000:cl=stereo',
           '-t', str(duration),
           '-acodec', 'pcm_s16le', output_file]
    subprocess.run(cmd, check=True)

def build_audio_timeline(file_list, date):
    audio_out_dir = f"{date}_audio"
    concat_list_path = f"{date}_audio.txt"
    os.makedirs(audio_out_dir, exist_ok=True)
    concat_entries = []

    for i, file_path in enumerate(file_list):
        base = Path(file_path).stem
        duration = get_duration(file_path)

        if has_audio(file_path):
            audio_path = os.path.join(audio_out_dir, f"{base}_audio.wav")
            extract_audio(file_path, audio_path)
            concat_entries.append(f"file '{audio_path}'")
        else:
            silence_path = os.path.join(audio_out_dir, f"{base}_silence.wav")
            create_silence(duration, silence_path)
            concat_entries.append(f"file '{silence_path}'")

    with open(concat_list_path, 'w') as f:
        f.write('\n'.join(concat_entries))

    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                    '-i', concat_list_path,
                    '-ar', '48000', '-ac', '2',
                    '-acodec', 'pcm_s16le', f"{date}.wav"],
                   check=True)
    os.system(f"rm {date}_audio.txt")
    shutil.rmtree(f"{date}_audio")