# Copy from SD Card

`bash src/copy/copy.sh ${sd_card_dir} ${yyyymmdd}`

## Multi-copy
If recordings over multiple days have accumulated, copy everything as,

`python src/copy/multiCopy.py -d ${yyyymmdd1} {yyyymmdd2...} -sd ${sd_card_dir}`