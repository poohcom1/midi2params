import warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys

if len(sys.argv) == 1:
    print("convert_midi [model] [DDSP] [midi] [outputfile]")
    exit()

import scipy.io.wavfile
from train_utils import midi2params, load_best_model, load_config, parse_arguments
from datasets import load_midi_file
import torch
from utils.util import load_ddsp_model
from utils.util import synthesize_ddsp_audio



midi_path = sys.argv[3]
model_path = sys.argv[1]

# This was for custom ouput
audio_file_name = sys.argv[4] if len(sys.argv) > 4 else None #''.join(os.path.basename(midi_file).split('.')[:-1]) + ".wav"

# get config
config = load_config('./midi2params/configs/midi2params-best.yml')

ckpt_path = sys.argv[2] or './checkpoints/CustomViolinCheckpoint'
ddsp_model = load_ddsp_model(ckpt_path)


midi_files = []

if os.path.isfile(midi_path):
    midi_files.append(midi_path)
else:
    for file in os.listdir(midi_path):
        midi_files.append(os.path.join(midi_path, file))

    print("Directory found! Converting %d files!" % len(midi_files))

for i, file in enumerate(midi_files):
    pitches, onset_arr, offset_arr = load_midi_file(file)

    batch = {}

    pitches = torch.Tensor([pitches])
    onset_arr = torch.Tensor([onset_arr])
    offset_arr = torch.Tensor([offset_arr])

    if torch.cuda.is_available():
        pitches = pitches.cuda()
        onset_arr = onset_arr.cuda()
        offset_arr = offset_arr.cuda()

    batch['pitches'] = pitches
    batch['onset_arr'] = onset_arr
    batch['offset_arr'] = offset_arr

    print("Getting params...")


    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        best_model = load_best_model(config, model_path)
        f0_pred, ld_pred = midi2params(best_model, batch)


    train_params = {
        'f0_hz': f0_pred[0],
        'loudness_db': ld_pred[0]
    }

    # Resynthesize parameters
    print("Resynthesizing...")
    new_model_resynth = synthesize_ddsp_audio(ddsp_model, train_params)

    file_name = audio_file_name
    if not audio_file_name:
        file_name = ''.join(os.path.basename(file).split('.')[:-1]) + ".wav"
    elif len(midi_files) > 1:
        file_name = ''.join(audio_file_name.split('.')[:-1]) + i + ".wav"
    else:
        file_name = audio_file_name

    scipy.io.wavfile.write(
        file_name, 16000, -new_model_resynth.swapaxes(0, 1)[0])
    print("Finished! Audio saved to %s." % file_name)
