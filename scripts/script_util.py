import os
import sys

# Disable
def block_print(msg=''):
    if msg != '': print(msg)
    sys.stdout = open(os.devnull, 'w')

# Restore
def enable_print(msg=''):
    if msg != '': print(msg)
    sys.stdout = sys.__stdout__