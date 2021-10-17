# Getting Started

Below are some commands you might want to run to get this repo set up and running. 
You can also just download the script file and run it to automate the process, run the command in the script one by one if you're worried about errors:

Prerequisites: 
 - python3.7
 - virtualenv

**MacOS and Linux**:
[setup_shell.sh](https://raw.githubusercontent.com/poohcom1/midi2params/main/setup_windows.bat)

**Windows**:
[setup_windows.bat](https://raw.githubusercontent.com/poohcom1/midi2params/main/setup_shell.sh)

*Note: The script itself clones the repo into a virtualenv, so don't run the the shell script from within an already cloned repo. 

To test the model out, `notebooks/midi2params-results.ipynb` is a demo notebook.

Also, check out the paper, currently hosted [here](https://cs.stanford.edu/~rjcaste/research/realistic_midi.pdf).

# Data Requirements:

## wav

|        Field        | Value  |
|---------------------|--------------|
|      codec_name     |  pcm_f32le   |
|      codec_type     |    audio     |
|   codec_tag_string  | [3][0][0][0] |
|      codec_tag      |    0x0003    |
|      sample_fmt     |     flt      |
|     sample_rate     |    16000     |
|       channels      |      1       |
|   bits_per_sample   |      32      |
|      time_base      |   1/16000    |
|       bit_rate      |    512092    |
|      nb_streams     |      1       |
|     nb_programs     |      0       |
|     format_name     |     wav      |
|     probe_score     |      99      |

# Training
Training requires 3 types of input data: midi files, wav files, and DDSP param files. 
The param files come in form of python pickle files, and can be automatically generated with an included script.

1. Prepare dataset of midi and wav files in the `data` directory (make one at project root if it does not exist).
   - Make sure corresponding midi and wav files have the same name
2. Split the files into 2 folders: `wav` and `midi`.
3. Run the `make_splits` script to automatically split the files into test/train/val folders:
```sh
python scripts/make_splits.py --path data/{date_set_folder}
```
4. Run the `extractor` script to automatically convert the wav files into params pickle files:
```sh
python scripts/extractor.py --path  data/{date_set_folder}/wav
```
5. Create a config yml file in `midi2params/configs`. You can just copy an existing one and just change the `dataset.dset_path` value to your dataset.

6. Run the `trainscript` file to train the model:
```sh
python midi2params/trainscript.py 
```

# File Structure Convention

Some of these may be mainly relevant if you're interested in training models.

## `configs/`

A folder that contains YAML config files for training models (MIDI -> parameters, parameters -> MIDI, etc.)

## `data/`

A folder containing the datasets to train on. Each folder under `data/` represents a distinct dataset. Each dataset `data/dataset` contains subfolders, such as `synth_params/` and `modified_midis/`. Then, under each of those is `train/`, `val/`, and `test/`. Under each of those are raw files---WAV files, MIDIs, or pickle files---that make up the meat of the dataset. The file names (excluding the extension) should be identical between the subfolders of a given dataset.

## `logs/`

Contains logs from runs training models. Each run is a folder under `logs/` that contains the best model so far, as well as losses over time, etc.

## `midi2params/`

Training script/utilities for our midi2param models.

## `notebooks/`

Catch-all for one-off and long-term Jupyter notebooks.

## `params/`

Model checkpoints from DDSP.

## `params2midi/`

Training script/utilities for our params2midi models.

## `scripts/`
Catch-all for one-off and long-term reusable scripts for data wrangling/manipulation.

### split_midis_into_arrs.py
Splits MIDI files into N seconds of pickle files


### split_midis.py
Splits MIDI files into smaller MIDI files given a length in seconds
 - `--length`, `-l`: Length in seconds to split into (default: 5)
 - `--sourcepath`, `-s`: Directory of MIDI files to split
 - `--targetpath`, `-t`: Target directory to save output files to

### split_saves.py
Splits wav files into smaller files given a length in seconds.

*Args same as above

### split_midis_into_arrs.py
Like `split_midis`, but outputs pickled files instead

*Args same as above

## `utils/`

Contains utility and convenience functions.
