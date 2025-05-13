import os
import subprocess
from src.utils.audio_utils import has_audio

def get_video_names(date, channels):
    all_names = []
    for channel in channels:
        channel_names = [file for file in os.listdir(channel)
                         if date in file]
        channel_names.sort()
        all_names.append(channel_names)
    
    return all_names


def writeText(fileList, dir, name):
    audio_source_list = []
    with open(name, "w") as f:
        for fileName in fileList:
            fileName = os.path.join(dir, fileName)
            audio_source_list.append(fileName)
            f.write(f"file {fileName} \n")
    f.close()

def deleteFilesFromList(fileList, dir):
    for fileName in fileList:
        fileName = os.path.join(dir, fileName)
        os.system(f"rm {fileName}")


def get_fps(filename):
    # Get raw FPS value like "18/1" or "25/1"
    cmd = ["ffprobe", "-v", "0", "-of", "csv=p=0",
           "-select_streams", "v:0",
           "-show_entries", "stream=r_frame_rate", filename]
    result = subprocess.run(cmd, capture_output=True, text=True)
    fps_str = result.stdout.strip()
    
    # Convert to float (e.g., "18/1" -> 18.0)
    if '/' in fps_str:
        fps_str = fps_str.split('\n')[0].split('/')[0]
    
    return float(fps_str)


def get_time_lapse_videos(channels):
    video_list = []
    for channel in channels:
        print(f"Looking for time lapses in {channel} channel...")
        channel_videos = os.listdir(channel)
        channel_videos.sort()
        for video in channel_videos:
            video_dir = os.path.join(channel, video)
            if get_fps(video_dir) < 24 and not has_audio(video_dir):
                video_list.append(video_dir)
    
    return video_list


def convert_fps_with_duration_change(input_file, output_file, target_fps=25):
    input_fps = get_fps(input_file)
    scale_factor = input_fps / target_fps
    vf_filter = f"setpts={scale_factor}*PTS,fps={target_fps}"
    
    cmd = ["ffmpeg", "-i", input_file,
           "-vf", vf_filter,
           "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-an",
           output_file]
    subprocess.run(cmd)

def fix_fps_from_dir_list(dir_list):
    for dir in dir_list:
        video_name = dir.split("/")[1]
        convert_fps_with_duration_change(dir, video_name, 25)
        os.system(f"mv {video_name} {dir}")

def fix_fps_from_idx_list(indices_list, channels, names):
    for indices, channel in zip(indices_list, channels):
        for i in range(len(indices)):
            file_name = f"{channel}/{names[channel][indices[i]]}"
            print(f"Fixing {i + 1}/{len(indices)} {file_name}...")
            video_fps = get_fps(file_name)
            if video_fps < 24.5:
                convert_fps_with_duration_change(file_name,
                                                 names[channel][indices[i]],
                                                 25)
                os.system(f"mv {names[channel][indices[i]]} {file_name}")


def change_duration(input_file, output_file, target_duration):
    # Get original duration
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', input_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    try:
        original_duration = float(result.stdout.strip())
    except ValueError:
        raise RuntimeError("Failed to get original duration")

    # Calculate PTS multiplier
    pts_multiplier = target_duration / original_duration

    # Run ffmpeg to change duration
    cmd = ["ffmpeg", "-y", "-i", input_file,
           "-filter:v", f"setpts={pts_multiplier}*PTS,fps=25",
           "-c:v", "libx264",
           "-preset", "slow",
           "-crf", "18",
           "-an", output_file]
    subprocess.run(cmd, check=True)


def stack_videos(front, back, left, right, output_file, w, h):
    cmd = ["ffmpeg", "-y", "-fflags", "+genpts", "-avoid_negative_ts", "make_zero",
           "-i", front, "-i", back, "-i", left, "-i", right,
           "-filter_complex",
           f"[0:v]scale={w}:{h},setpts=PTS-STARTPTS[top_left];"
           f"[1:v]scale={w}:{h},setpts=PTS-STARTPTS[top_right];"
           f"[2:v]hflip,scale={w}:{h},setpts=PTS-STARTPTS[bottom_right];"
           f"[3:v]hflip,scale={w}:{h},setpts=PTS-STARTPTS[bottom_left];"
           f"[top_left][top_right]hstack=inputs=2[top];"
           f"[bottom_left][bottom_right]hstack=inputs=2[bottom];"
           f"[top][bottom]vstack=inputs=2[video]",
           "-map", "[video]", "-map", "2:a?",
           "-video_track_timescale", "12800",
           "-c:v", "libx264", "-crf", "23", "-preset", "fast",
           "-an", output_file]
    subprocess.run(cmd, check=True)