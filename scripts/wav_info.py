import sys
import os
from prettytable.prettytable import MARKDOWN
from pydub.utils import mediainfo
from prettytable import PrettyTable

file = sys.argv[1]
excluded_data = ['DISPOSITION', 'filename', 'codec_long_name', 'index', 'TAG', 'format_long_name']

def print_wav_data(files, excluded_data=excluded_data):
    fields = [f for f in mediainfo(files[0]).keys() if f not in excluded_data]

    table = PrettyTable()
    table.set_style(MARKDOWN)
    table.field_names = ["Field", *[os.path.basename(file) for file in files]]

    infos = [mediainfo(file) for file in files]

    
    for key in fields:
        row = [key]

        for info in infos:
            row.append(info[key])

        table.add_row(row)

    print(table)

print_wav_data(sys.argv[1:])
