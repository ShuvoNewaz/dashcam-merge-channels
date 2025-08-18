# Copy from SD Card

The filenames do not correspond to the actual time the files were created. However, the files preserve the actual end time of the video. By extracting the end time and the duration, the start time can be determined. The following copies the files to from the sd card to the local directory and renames them to their actual start times.

`python3 -m src.copy.copy -d ${date} -sd ${sd_card_dir}`