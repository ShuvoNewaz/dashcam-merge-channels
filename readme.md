# Environment

This project was developed in an Ubuntu 22.04 system. Tools required:

- Python
- FFMpeg
- FFProbe
- Exiftool

To use, open terminal in your preferred work directory and enter the following command:

`git clone https://github.com/ShuvoNewaz/dashcam-merge-channels.git`

`cd dashcam-merge-channels`

# Simplified

Run `bash main.sh ${sd_card_dir} ${parallel} ${yyyymmdd1} ${yyyymmdd2}...`

If you wish to understand how each component works, look for the readmes inside corresponding src directory. The sequence is:

- Copy from sd card.
- Split time lapse videos if they cross midnight.
- Fix the time lapse frame rate and duration.
- Merge individual channel videos.
- Make channel videos the same duration.
- Stack same duration videos.

# File Management

Given the number of channels, the total space required during each transition stage grows very large very fast. This is why the videos from the previous stage are deleted as soon as the videos in the current stage are generated. The video names and directories in every stage are listed below:

- Inside individual `{channel}` directory after copying from sd card.
- Inside individual `{channel}` directory after fixing time lapse frame rate.
- Inside individual `{channel}` directory after addressing time lapse midnight crosses.
- In root directory after merging. The file names are `{channel}_{date}_temp.ts`. The videos inside the channel directories are deleted. The generated audio file is `{date}.wav`.
- In root directory after making all 4 channels the same duration. The file names are `{channel}_{date}.ts`. `{channel}_{date}_temp.ts` are deleted.
- In root directory after stacking. The file name is `{date}_no_audio.ts`. `{channel}_{date}.ts` are deleted.
- In root directory after adding audio. The final file name is `{date}.ts`. `{date}_no_audio.ts` and `{date}.wav` are deleted.

# Parallel/Series Operation

Parallel operation saves time, but requires more disk space to process all the channels at once. Series operation requires more time, but can work when disk space is a constraint (long trips).