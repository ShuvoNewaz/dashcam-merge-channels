# Copy from SD Card

`bash copy.sh ${yyyymmdd} ${sd_card_dir}`

## Multi-copy

`python multiCopy.py -d ${yyyymmdd1 yyyymmdd2...} ${sd_card_dir}`

# Time Lapse

The front channel records time lapse at 18 FPS, the others at 25 FPS. Change the front time lapses to 25 FPS as follows (other channels too if needed). The indices are zero-indexed.

`python fix_timelapse -c Front -i ${front_time_lapse_indices} -c Back -i ${back_time_lapse_indices}...`

The above script will automatically replace the 18 FPS time lapse videos with the correct ones.

# Merge and Stack

Because of time lapse frame rate and other minor issues, there may be different number of videos recorded in different channel, with front channel video count likely being higher than the rest. Use channel-specific start and end indices for that particular date.

`python merge.py -d ${date} -fs ${start_video_index_front} -fe ${end_video_index_front} ... -rs ${start_video_index_right} -re ${end_video_index_right}`

## Multi-merge

`python multiMerge.py -d ${date1} -fs ${start_video_index_front1} -fe ${end_video_index_front1} ... -rs ${start_video_index_right2} -re ${end_video_index_right2} -d ${date2} -fs ${start_video_index_front2} -fe ${end_video_index_front2} ... -rs ${start_video_index_right2} -re ${end_video_index_right2}...`