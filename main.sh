#!/bin/bash
clear

sd_card_dir="$1"
for date in "${@:2}"; # must be yyyymmdd
do
    # Copy from sd card
    bash src/copy/copy.sh ${date} ${sd_card_dir}

    # Fix time lapse videos
    python3 -m src.time_lapse.fix_timelapse

    # Check if time lapse crosses midnight
    python3 -m src.time_lapse.midnight_split -d ${date} -sd ${sd_card_dir}

    # Merge and stack
    python3 -m src.merge.merge_channel_videos -d ${date}
    python3 -m src.merge.fix_duration -d ${date}
    python3 -m src.merge.stack -d ${date}
done