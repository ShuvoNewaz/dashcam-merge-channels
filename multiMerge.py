import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dates", nargs='+', type=str, required=True)
parser.add_argument("-i", "--indices_list", nargs='+', action="append", type=int, required=True)
args = parser.parse_args()

for date, indices in zip(args.dates, args.indices_list):
    indices_str = ' '.join(map(str, indices))
    os.system(f"python merge.py -i {indices_str} -d {date}")