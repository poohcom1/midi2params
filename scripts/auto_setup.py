import os
import sys
import shutil
from script_util import block_print, enable_print

#  Args
main_dir = sys.argv[1]
os.chdir(main_dir)

# Config
wav_dir = 'wav'
mid_dir = 'midi'
param_dir = 'params'

# Split and move
files = os.listdir()

if wav_dir not in files:
    os.mkdir(wav_dir)

if mid_dir not in files:
    os.mkdir(mid_dir)


#  Split
import split_midis_into_arrs

args = lambda: None
args.length = 5
args.sourcepath = os.path.curdir
args.targetpath = os.path.join(os.path.curdir, mid_dir)

block_print("Splitting midis into pickle files...")
split_midis_into_arrs.main(args)
enable_print()

import split_wavs

args.length = 5
args.sourcepath = os.path.curdir
args.targetpath = os.path.join(os.path.curdir, wav_dir)

block_print("Splitting wavs...")
split_wavs.main(args)
enable_print()

# Params
import extractor
import multiprocessing

total_workers = multiprocessing.cpu_count()
wav_path = os.path.join(os.path.curdir, wav_dir)

# get all files that we need to convert
allfiles = []
for (dirpath, dirnames, filenames) in os.walk(wav_path):
    allfiles += [os.path.join(dirpath, file) for file in filenames]
fl = sorted(allfiles)

print("Extracting params")

processes = []
for i in total_workers:
    # get all files that we need to convert
    allfiles = []
    for (dirpath, dirnames, filenames) in os.walk(wav_path):
        allfiles += [os.path.join(dirpath, file) for file in filenames]
    fl = sorted(allfiles)

    fl = fl[i::total_workers]

    def extract_multiple():
        for idx, file in enumerate(fl):
            print('worker #{}: {} / {}'.format(i, idx, len(fl)))
            # NOTE: The extract function is stateful but here we want stateless behavior and
            # multiprocessing.Process is a quick way of achieving this
            extractor.extract(file, wav_path)

    p = multiprocessing.Process(target=extract_multiple)
    p.start()
    processes.append(p)

for p in processes:
    p.join()


print("Done!")



