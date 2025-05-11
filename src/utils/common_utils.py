import subprocess


def get_duration(path):
    cmd = ["ffprobe",
           "-v", "error",
           "-select_streams", "v:0",
           "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1",
           path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None  # or raise an exception
