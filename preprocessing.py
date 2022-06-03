import tensorflow as tf
import os
import pandas as pd
import numpy as np

# An integer scalar Tensor. The window length in samples.
frame_len = 512 * 2
# An integer scalar Tensor. The number of samples to step.
frame_step = 320 * 2
# An integer scalar Tensor. The size of the FFT to apply.
# If not provided, uses the smallest power of 2 enclosing frame_len.
fft_len = 768 * 2


def calltimes_to_labels(fname_labels, samplerate=96000):
    """
    """
    label_times = pd.read_csv(fname_labels)

    fnames_wav = label_times['filename_wav'].unique()

    labels = {}
    for fname_wav in fnames_wav:
        ids = label_times[label_times['filename_wav'] == fname_wav].index
        n_samples = int(samplerate * label_times.loc[ids[0], 'wav_duration'])
        lbls = np.zeros((n_samples, 2), dtype=np.uint16)

        for idx in ids:

            i0 = int(label_times.loc[idx, 'time_on'] * samplerate)
            i1 = int(label_times.loc[idx, 'time_off'] * samplerate)
            call_type = label_times.loc[idx, 'call_type']
            caller_id = label_times.loc[idx, 'caller_id']
            lbls[i0: i1, 0] = call_type
            lbls[i0: i1, 1] = caller_id

        labels[fname_wav] = lbls

    return labels


def encode_single_sample(fname_wav, labels):
    """
    fname_wav -
    labels    -

    """
    ###########################################
    # Process the Audio
    ###########################################
    # 1. Read wav file
    f = tf.io.read_file(fname_wav)
    # 2. Decode the wav file
    audio, samplerate = tf.audio.decode_wav(f)
    audio = tf.squeeze(audio, axis=-1)
    # 3. Change type to float
    audio = tf.cast(audio, tf.float32)
    # 4. Get the spectrogram
    spectrogram = tf.signal.stft(audio,
                                 frame_len=frame_len,
                                 frame_step=frame_step,
                                 fft_len=fft_len)
    # 5. We only need the magnitude, which can be derived by applying tf.abs
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.pow(spectrogram, 0.5)
    # 6. normalisation
    means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)

    return spectrogram, labels[fname_wav.split(os.path.sep)[-1]]
