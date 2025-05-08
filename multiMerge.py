import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dates", action="append",
                    type=str, required=True)
parser.add_argument("-s", "--start_list", action="append",
                    type=int, required=True)
parser.add_argument("-e", "--end_list", action="append",
                    type=int, required=True)
args = parser.parse_args()

for date, start, end in zip(args.dates, args.start_list, args.end_list):
    os.system(f"python merge.py -s {start} -e {end} -d {date}")
