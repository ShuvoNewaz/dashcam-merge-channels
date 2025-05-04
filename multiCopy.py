import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dates", nargs='+', type=str, required=True)
args = parser.parse_args()

for date in args.dates:
    os.system(f"bash copy.sh {date}")