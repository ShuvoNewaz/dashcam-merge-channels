# Time Lapse

The channels don't always record time lapse in 25 FPS. Moreover, different channels sometimes record in different frame rates. The time lapses need to be the same frame rate and duration for proper synchronization.

## From Indices

The time low frame-rate time lapses are detected by computing the frame rate of all the videos and checking if they have audio. If a video has a low frame rate and no audio, it will be classified as a time lapse. However, if the microphone was accidentally turned off, regular videos may also be classified as time lapse. This [file](src/time_lapse/fix_timelapse_from_indices.py) allows manual selection of indices of time lapse videos in each channel. If this is used, [`main.sh`](main.sh) must be modified accordingly. An example modification is shown below:

`front_lapse_indices="5 6 7 19 26 30 31 32 33 34 35 36 37 38 41 44"`

`back_lapse_indices="5 6 18 25 29 30 31 32 33 34 35 38 41"`

`left_lapse_indices="5 6 18 25 29 30 31 32 33 34 35 38 41"`

`right_lapse_indices="5 6 18 25 29 30 31 32 33 34 35 38 41"`

`python -m src.time_lapse.fix_timelapse_from_indices -c Front -i ${front_lapse_indices} -c Back -i ${back_lapse_indices} -c Left -i ${left_lapse_indices} -c Right -i ${right_lapse_indices}`

## Automated

If the microphone was not turned off, simply enter

`python -m src.time_lapse.fix_timelapse`

## Midnight Crossing

The way the scripts are automated, the videos with the same date tag in their file names are merged and stacked. Since different channels have different frame rates, the channel durations can go out of sync when time lapses cross midnight. This is addressed by splitting the time lapse videos at midnight as follows:

`python -m src.time_lapse.midnight_split -d ${date} -sd ${sd_card_dir}`

### Caution

The sd card must not be removed before this part is completed. Also, the midnight crossing script must not be run more than once unless the source files are copied again. This is because the file creation metadata of the original file in the sd card is used to compute how much of the time lapse has gone over to the next day. Once split, running this again will mess up the split.