import os

import sys

def verify_count(path: str):
    path_dict = {}
    subsets = set()

    for folder in os.listdir(path):
        if not os.path.isdir(os.path.join(path, folder)): continue

        path_dict[folder] = {}
        for subset in os.listdir(os.path.join(path, folder)):
            if not os.path.isdir(os.path.join(path, folder, subset)): continue

            subsets.add(subset)
            path_dict[folder][subset] = len(os.listdir(os.path.join(path, folder, subset)))

    data_error = False

    for subset in list(subsets):
        print("%s dataset: " % subset, end="")
        for folder in os.listdir(path):
            if not os.path.isdir(os.path.join(path, folder)): continue
            
            print("%s files, " % path_dict[folder][subset], end="")

        print()

    return data_error

if __name__ == "__main__":
    path = sys.argv[1]

    verify_count(path)