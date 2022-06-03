import scipy.io
import h5py
from scipy.io import wavfile
import numpy as np
import os
import glob
import csv

DATA_DIR = f'{os.path.expanduser("~")}/Python/MarmosetCallClassification/data'


def audiolen_to_specgramlen(audio_len, frame_len, frame_step):
    """
    WRONG when audio_len / frame_step has a reminder of .6
    WHY?
    
    Test:
    ----

    1.
        audio_len = 60377280
        spectrogram.shape = (90144, 769)
        specgram_len == 94338

    2.
        audio_len = 57692544
        spectrogram.shape = (90144, 769)
        specgram_len == 90143
    3.
        audio_len = 59538816
        spectrogram.shape = (93028, 769)
        specgram_len == 93028
    4.
        audio_len = 60273024
        spectrogram.shape = (94176, 769)
        specgram_len == 94175
    5.
        audio_len = 60273024
        spectrogram.shape = (94338, 769)
        specgram_len == 94338
    """

    specgram_len = int(audio_len / frame_step) - 1

    return specgram_len


def convertfiles_mat_to_wav(mat_dir, wav_dir, fname_labels):
    """
    Arguments
    ---------
    mat_dir      : directory with MAT files to convert to WAV.
    wav_dir      : directory where the WAV files should be written.
    fname_labels : file name of CSV file where the labels will be written.
                   If it is an existing file then the labels will be appended
                   at the end, otherwise a new file will be created and
                   written to.
    """
    fnames_mat = get_filenames(mat_dir)

    for fname_mat in fnames_mat:
        for fn_sound in fname_mat['sound']:
            fname_wav = fn_sound.split(os.sep)[-1].replace('.mat', '.wav')
            samplerate, duration = mat_to_wav(fn_sound,
                                              f'{wav_dir}{os.sep}{fname_wav}')

            labels = read_mat_labels(fname_mat['label'],
                                     fname_wav,
                                     samplerate,
                                     duration)
            if len(labels):
                write_labels_to_csv(fname_labels, labels)


def read_mat_labels(fname, fname_wav, samplerate, wav_duration):
    """
    Reads MAT files with labels into a labels list for
    subsequent writing to csv.

    Argument
    --------
    fname       : File name of MAT file with labels
    fname_mat   : File name of the WAV file with audio.
    samplerate  : samplerate

    Return
    ------
    labels : list of dicts holding the label data.
             See write_labels_to_csv() for details.
    """
    f = scipy.io.loadmat(fname)

    fname_wav = fname_wav.split(os.sep)[-1]

    if not all(key in f.keys() for key in ['TypeofCallTag',
                                           'TotCallsBegFinal',
                                           'TotCallsEndFinal',
                                           'CallerIDTag']):

        print(f'Skipping {fname}\n\tkeys missing; available: {f.keys()} .')
        return []

    call_types = f['TypeofCallTag'].flatten()
    # 'cx' is an initial offset in the beginning that used when annotating.
    onsets = (f['TotCallsBegFinal'] / samplerate + f['cx']).flatten()
    offsets = (f['TotCallsEndFinal'] / samplerate + f['cx']).flatten()
    caller_ids = (f['CallerIDTag']).flatten()

    n = len(call_types)

    assert all(len(ar) == n for ar in [onsets, offsets, caller_ids])

    labels = []
    for i in range(n):
        if not any(np.isnan([onsets[i],
                             offsets[i],
                             call_types[i],
                             caller_ids[i]])):

            labels.append({'filename_wav': fname_wav,
                           'time_on': onsets[i],
                           'time_off': offsets[i],
                           'call_type': int(call_types[i]),
                           'caller_id': int(caller_ids[i]),
                           'wav_duration': wav_duration})

    return labels


def write_labels_to_csv(fname, labels):
    """
    Arguments
    ---------
    fname  : file name of CSV to write to. If the file already exists then rows
             are appended, otherwise a new file is created.
    labels : a list of dicts, where the dicts have the following keys:
        filename : (string) file name of the corresponding wavfile.
        time_on  : (float) time for onset of call in seconds.
        time_off : (float) time for offset of call in seconds.
        call_type: (int) phee: 49; twitter: 50; trill: 51; cry: 52;
                         subharmonic phee: 53; cry-phee: 54.
        caller_id: (int) identity of the caller.
        wav_duration: (float) the duration of the recording
    """
    if os.path.isfile(fname):
        mode = 'a'
        print(f'Appending to {fname}')
    else:
        mode = 'w'
        print(f'Creating and writing to {fname}')

    with open(fname, mode, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=labels[0].keys())
        if mode == 'w':  # write the header only if it is a newly created file.
            writer.writeheader()

        writer.writerows(labels)


def get_filenames(base_dir):
    """
    Returns a list of matched sound and label files in dicts.
    """
    # fnames = {'sound': [], 'label': []}
    # for fname in glob.iglob(f'{base_dir}/**', recursive=True):
    #     if fname.endswith('results.mat'):
    #         fnames['label'].append(fname)
    #     elif fname.endswith('.mat'):
    #         fnames['sound'].append(fname)

    fnames = []
    putative_fnames = glob.glob(f'{base_dir}/**', recursive=True)
    for fname in putative_fnames:
        if fname.endswith('results.mat'):
            label_fname = fname
            record_name = label_fname.split(os.sep)[-1].rstrip('_results.mat')
            sound_fnames = []
            for fname in putative_fnames:
                if record_name in fname and fname != label_fname:
                    sound_fnames.append(fname)

            if len(sound_fnames):
                fnames.append({'sound': sound_fnames,
                               'label': label_fname})
            else:
                print(f'Skipping {record_name}; sound file missing.')

    return fnames


def mat_to_wav(fname_mat, fname_wav):
    """
    Convert 96 kHz float (-1. to 1.) MAT files to
    96 kHz int16 WAV (-32767 to 32767) files.
    """

    max_amplitude = np.iinfo(np.int16).max

    with h5py.File(fname_mat, 'r') as f:
        if 'y' in f.keys():
            y = f['y'][0] * max_amplitude
        elif 'ShortY' in f.keys():
            y = f['ShortY'][0]
        else:
            print(f'''Sound seems to be missing from {fname_mat}.
                      Keys: {f.keys()}''')
            return

        samplerate = int(f['Fs'][0])
        duration = np.max(y.shape) / samplerate
        wavfile.write(fname_wav,
                      samplerate,
                      (y * max_amplitude).astype(np.int16))

        return samplerate, duration
