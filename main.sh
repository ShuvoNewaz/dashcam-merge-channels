clear

# Address time lapse issues
front_lapse_indices="3 6 9 10 15 19 20 25 37 38 39 40 41 53"
back_lapse_indices="2 5 8 13 17 18 23 35 36 37 38 50"
left_lapse_indices="3 6 9 14 18 19 24 36 37 38 39 51"
right_lapse_indices="3 6 9 14 18 19 24 36 37 38 39 51"
python -m src.fix_timelapse \
-c Front -i ${front_lapse_indices} \
-c Back -i ${back_lapse_indices} \
-c Left -i ${left_lapse_indices} \
-c Right -i ${right_lapse_indices}

# Merge and stack
date=2025-05-10
parse_args="-d ${date} -fs 0 -fe 54 -bs 0 -be 51 -ls 0 -le 52 -rs 0 -re 52"
python -m src.merge.merge_channel_videos ${parse_args}
python -m src.merge.fix_duration.py ${parse_args}
python -m src.merge.stack -d ${date}
