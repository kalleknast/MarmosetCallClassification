import scipy.io
import h5py
import tensorflow as tf
from scipy.io import wavfile
import numpy as np
import os
import glob

DATA_DIR = f'{os.path.expanduser("~")}/Python/MarmosetCallClassification/data'


def convertfiles_mat_to_wav(mat_dir, wav_dir):
    """
    """
    fnames_mat = get_filenames(mat_dir)

    for fname_mat in fnames_mat['data']:
        fname_wav = fname_mat.split('/')[-1].replace('.mat', '.wav')
        # import ipdb; ipdb.set_trace()
        mat_to_wav(fname_mat, f'{wav_dir}/{fname_wav}')


def get_filenames(base_dir):
    """
    """
    fnames = {'data': [], 'labels': []}
    for fname in glob.iglob(f'{base_dir}/**', recursive=True):
        if fname.endswith('results.mat'):
            fnames['labels'].append(fname)
        elif fname.endswith('.mat'):
            fnames['data'].append(fname)

    return fnames


def mat_to_wav(fname_mat, fname_wav):
    """
    Convert 96 kHz float (-1. to 1.) MAT files to
    96 kHz int16 WAV (-32767 to 32767) files.
    """

    max_amplitude = np.iinfo(np.int16).max

    with h5py.File(fname_mat, 'r') as f:
        y = f['y'][0] * max_amplitude
        samplerate = int(f['Fs'][0])
        wavfile.write(fname_wav, samplerate, y.astype(np.int16))
