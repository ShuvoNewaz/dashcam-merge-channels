# Copy from SD Card

`bash copy.sh ${yyyymmdd} ${sd_card_dir}`

## Multi-copy
If recordings over multiple days have accumulated, copy everything as,

`python multiCopy.py -d ${yyyymmdd1 yyyymmdd2...} ${sd_card_dir}`

# Time Lapse

The channels don't always record time lapse in 25 FPS. Moreover, different channels sometimes record in different frame rates. The time lapses need to be the same frame rate and duration for proper synchronization.

# Merge and Stack

Because of time lapse frame rate and other minor issues, there may be different number of videos recorded in different channel, with front channel video count likely being higher than the rest. Use channel-specific start and end indices for that particular date.

# Execution

Edit [main.sh](main.sh) as follows:

- Enter zero-indexed indices of time lapse videos of the respective channels in `${channel}_lapse_indices`.
- Enter `date`. Format doesn't matter.
- Enter zero-indexed start and end indices of every channel on that date in `parse_args`. For example, `-fs` is the start index of the front channel.

Enter information for multiple dates in order if needed. From the root directory, enter

`bash main.sh`