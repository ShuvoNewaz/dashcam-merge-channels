import os
import subprocess
from datetime import datetime, timedelta
from src.utils.common_utils import get_duration
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


def is_timelapse(video_dir):

    return get_fps(video_dir) < 24 and not has_audio(video_dir)


def get_time_lapse_videos(channels):
    video_list = []
    for channel in channels:
        print(f"Looking for time lapses in {channel} channel...")
        channel_videos = os.listdir(channel)
        channel_videos.sort()
        for video in channel_videos:
            video_dir = os.path.join(channel, video)
            if is_timelapse(video_dir):
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


def format_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_modification_time_from_exif(file_path):
    result = subprocess.run(
        ["exiftool", "-FileModifyDate", file_path],
        capture_output=True,
        text=True,
        check=True
    )
    output = result.stdout.strip()
    output = output.split(":")[1:6]
    output[0] = output[0][1:]
    output.insert(3, output[2][-2:])
    output[2] = output[2][:2]
    output[5] = output[5][:2]
    
    return f"{output[0]}-{output[1]}-{output[2]} {output[3]}:{output[4]}:{output[5]}"


def split_at_midnight(video_path: str,
                      sd_card_dir):
    channel, video_name = video_path.split("/")
    channel_abbr = {"front": "F", "back": "R",
                    "left": "FL", "right": "FR"}
    src_video_dir = f"{sd_card_dir}/video/{channel_abbr[channel]}/{video_name}"
    end_time_str = get_modification_time_from_exif(src_video_dir)
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    duration_sec = get_duration(video_path)
    fps = get_fps(video_path)
    start_time = end_time - timedelta(seconds=duration_sec*fps)

    # Compute next midnight
    midnight = (start_time + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    date2 = str(midnight.date())
    date2 = date2.replace("-", "")

    if end_time <= midnight:
        print("Video does not cross midnight. No split needed.")
        return None

    # Compute offset in seconds from start to midnight
    split_offset = (midnight - start_time).total_seconds() / fps

    base, ext = os.path.splitext(video_path)
    
    out1 = video_name
    out2 = f"{date2}_000000{channel_abbr[channel]}{ext}"

    print(f"Splitting at midnight: {midnight.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Part 1 duration: {split_offset:.2f} seconds")

    # Run ffmpeg commands
    subprocess.run(["ffmpeg", "-y", "-i", video_path, "-t", str(split_offset), "-c", "copy", out1])
    subprocess.run(["ffmpeg", "-y", "-ss", str(split_offset), "-i", video_path, "-c", "copy", out2])

    # Move to channel directory
    os.system(f"mv {out1} {video_path}")
    os.system(f"mv {out2} {channel}/{out2}")

    return out1, out2