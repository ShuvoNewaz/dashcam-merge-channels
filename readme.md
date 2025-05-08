# Copy from SD Card

`bash copy.sh ${yyyymmdd} ${sd_card_dir}`

## Multi-copy

`python multiCopy.py -d ${yyyymmdd1 yyyymmdd2...} ${sd_card_dir}`

# Time Lapse

The front channel records time lapse at 18 FPS, the others at 25 FPS. Change the front time lapses to 25 FPS as follows (other channels too if needed). The indices are zero-indexed

`python fix_timelapse -c Front -i ${front_video_indices} -c Back -i ${back_video_indices}...`

The above script will automatically replace the 18 FPS time lapse videos with the correct ones.

# Merge and Stack

`python merge.py -d ${date} -s {start_video_index} -e {end_video_index}`

## Multi-merge

`python multiMerge.py -d ${date1} -s {start_video_index1} -e {end_video_index1} -d ${date2} -s {start_video_index2} -e {end_video_index2}...`