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

Run `bash main.sh ${sd_card_dir} ${yyyymmdd1} ${yyyymmdd2}...`

If you wish to understand how each component works, look for the readmes inside corresponding src directory. The sequence is:

- Copy from sd card.
- Fix the time lapse frame rate and duration.
- Split time lapse videos if they cross midnight.
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

## Parallel Operation

In the stage where the channels are all forced to the same duration, all 4 channels are done simultaneously (in parallel). During this process, all 4 `{channel}_{date}_temp.ts` and the growing `{channel}_{date}.ts` files exist in the disk at the same time. Depending on the length of the recording on the day, the space requirement can be ridiculously high (100GB for 3 hours of video). A series operation may be preferred if disk space is a constraint.

## Series Operation

The video duration stage is performed one channel at a time. `{channel}_{date}_temp.ts` is deleted as soon as its corresponding `{channel}_{date}.ts` is generated. This version of the repository does not support the series operation.

### Using Previous Commit

To do this stage in series, please move to a previous commit by entering

`git checkout 9a713e8`

right after cloning and changing directory. Follow the next steps are outlined above. Series operation saves space, but needs much more time to complete.

### Staying in Current Commit

The current contents of [this](src/merge/fix_duration.py) file can be replaced by [this](https://github.com/ShuvoNewaz/dashcam-merge-channels/blob/9a713e8ba0fb1ed29753b5df49d0054890df51a2/src/merge/fix_duration.py) file to perform series operation.