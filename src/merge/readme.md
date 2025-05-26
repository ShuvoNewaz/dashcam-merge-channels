# Merge and Stack

Because of time lapse frame rate and other minor issues, there may be different number of videos recorded in different channel, with front channel video count likely being higher than the rest.

The videos from individual channels are first concatenated as follows:

`python -m src.merge.merge_channel_videos -d ${date} -p {parallel}`

The argument `p` determines the mode of channel operation (parallel/series). `p` is either `True` or `False`. The channels video lengths are slightly off from each other. This difference is reconciled as,

`python -m src.merge.fix_duration.py -d ${date} -p {parallel}`

The same length videos are stacked.

`python -m src.merge.stack -d ${date}`