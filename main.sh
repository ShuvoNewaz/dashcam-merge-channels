#!/bin/bash
clear

sd_card_dir="$1"
parallel="$2" # True/False
for date in "${@:3}"; # must be yyyymmdd
do
    # Copy from sd card
    python3 -m src.copy.copy -d ${date} -sd ${sd_card_dir}

    # Check if time lapse crosses midnight
    python3 -m src.time_lapse.midnight_split -d ${date}

    # Fix time lapse videos
    python3 -m src.time_lapse.fix_timelapse   

    # Merge and stack
    python3 -m src.merge.merge_channel_videos -d ${date} -p ${parallel}
    python3 -m src.merge.fix_duration -d ${date} -p ${parallel}
    python3 -m src.merge.stack -d ${date}
done
