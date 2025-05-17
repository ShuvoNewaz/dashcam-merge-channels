# Environment

This project was developed in an Ubuntu 22.04 system. Tools required:

- Python
- FFMpeg
- FFProbe
- Exiftool

# Simplified

Run `bash main.sh ${sd_card_dir} ${yyyymmdd1} ${yyyymmdd2}...`

If you wish to understand how each component works, look for the readmes inside corresponding src directory. The sequence is:

- Copy from sd card.
- Fix the time lapse frame rate and duration.
- Split time lapse videos if they cross midnight.
- Merge individual channel videos.
- Make channel videos the same duration.
- Stack same duration videos.