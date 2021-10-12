import os
import pydub
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate fles training dataset randomly (or add to a pre-existing one).')

    parser.add_argument('--sourcepath', '-s', type=str, default='',
                        help='Path to the source Lakh dataset (as is after extracting tar file)')
    parser.add_argument('--targetpath', '-t', type=str,
                        default='', help='Path to the target dataset path')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_arguments()

    files = [f for f in os.listdir(args.sourcepath) if '.wav' in f]

    output_dir = args.targetpath or args.sourcepath

    count = 0

    print('Converting')
    for f in files:
        input_path = os.path.join(args.sourcepath, f)
        audio = pydub.AudioSegment.from_wav(input_path)

        audio = audio.set_frame_rate(16000)
        audio.export(os.path.join(output_dir, f), format="wav", bitrate=16000)

        print('.', end='')

        count += 1

    print("\nConverted %d files!" % (count))
