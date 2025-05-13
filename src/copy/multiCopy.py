import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dates", nargs='+', type=str, required=True)
parser.add_argument("-sd", "--sd_card_dir", type=str, required=True)
args = parser.parse_args()

for date in args.dates:
    os.system(f"bash src/copy/copy.sh {date} {args.sd_card_dir}")