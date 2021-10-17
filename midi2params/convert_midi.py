import warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import scipy.io.wavfile
from train_utils import midi2params, load_best_model, load_config, parse_arguments
from datasets import load_midi_file
import torch
from utils.util import load_ddsp_model
from utils.util import synthesize_ddsp_audio

midi_file = sys.argv[1]
model_path = './model/best_model.pt'
audio_file_name = ''.join(os.path.basename(midi_file).split('.')[:-1]) + ".wav"


# get config
config = load_config('./midi2params/configs/midi2params-best.yml')

ckpt_path = './checkpoints/CustomViolinCheckpoint'
ddsp_model = load_ddsp_model(ckpt_path)


pitches, onset_arr, offset_arr = load_midi_file(midi_file)

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

scipy.io.wavfile.write(audio_file_name, 16000, -new_model_resynth.swapaxes(0, 1)[0])
print("Finished! Audio saved to %s." % audio_file_name)
