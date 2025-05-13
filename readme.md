# Simplified

Run `bash main.sh ${sd_card_dir} ${yyyymmdd1} ${yyyymmdd2}...`

If you wish to understand how each components work, look for the readmes inside corresponding src directory. The sequence is:

- Copy from sd card.
- Fix the time lapse frame rate and duration.
- Merge individual channel videos.
- Make channel videos the same duration.
- Stack same duration videos.