clear

# Address time lapse issues
front_lapse_indices="7 8 9 13 18 19 20 21 22 23 24 25 26 27 28 35 36 44"
other_lapse_indices="7 8 12 17 18 19 20 21 22 23 24 25 26 27 34 35 43"
python -m src.fix_timelapse \
-c Front -i ${front_lapse_indices} \
-c Back -i ${other_lapse_indices} \
-c Left -i ${other_lapse_indices} \
-c Right -i ${other_lapse_indices}

# Merge and stack
date=2025-05-09
parse_args="-d ${date} -fs 0 -fe 45 -bs 0 -be 44 -ls 0 -le 44 -rs 0 -re 44"
python -m src.merge.merge_channel_videos ${parse_args}
python -m src.merge.fix_duration.py ${parse_args}
python -m src.merge.stack -d ${date}