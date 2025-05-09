import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dates", action="append",
                    type=str, required=True)
parser.add_argument("-fs", "--front_start_list", action="append",
                    type=int, required=True)
parser.add_argument("-fe", "--front_end_list", action="append",
                    type=int, required=True)
parser.add_argument("-bs", "--back_start_list", action="append",
                    type=int, required=True)
parser.add_argument("-be", "--back_end_list", action="append",
                    type=int, required=True)
parser.add_argument("-ls", "--left_start_list", action="append",
                    type=int, required=True)
parser.add_argument("-le", "--left_end_list", action="append",
                    type=int, required=True)
parser.add_argument("-rs", "--right_start_list", action="append",
                    type=int, required=True)
parser.add_argument("-re", "--right_end_list", action="append",
                    type=int, required=True)
args = parser.parse_args()

for date, \
    front_start, front_end, \
    back_start, back_end, \
    left_start, left_end, \
    right_start, right_end in \
    zip(args.dates,
        args.front_start_list, args.front_end_list,
        args.back_start_list, args.back_end_list,
        args.left_start_list, args.left_end_list,
        args.right_start_list, args.right_end_list):
    os.system(f"python merge.py -d {date} \
              -fs {front_start} -fe {front_end} \
                -bs {back_start} -be {back_end}\
                -ls {left_start} -le {left_end}\
                -rs {right_start} -re {right_end}")
