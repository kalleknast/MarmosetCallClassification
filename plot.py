#!/usr/bin/env python3
'''
Plotting for MarmosetCallClassification
'''
import argparse
import os.path as osp
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import convert_annotation_codes
from matplotlib.patches import Rectangle


# plt.ion()
plt.ioff()


def plot_predictions(annot_csv_path, spec_dir, fig_dir, plot_dur=10,
                     mark_onset=True, mark_offset=True):
    '''
    Plots spectrograms annotated with the predicted
    calls (onset/offset and call type).
    Used to visually inspect the output from "vak predict predict.toml".
    The resulting PNG images are saved to "fig_dir".


    Arguments
    ---------
    annot_csv_path  : relative or absolute path to the CSV file returned by
                      "vak predict predict.toml".
                      I.e. output_dir + annot_csv_filename in predict.toml.
    spec_dir        : The directory where the spectrograms returned by
                      "vak prep predict.toml" are stored.
    fig_dir         : The directory where to resulting PNG images will be stored.
    plot_dur        : Duration (in seconds) to plot in each figure.
                      Default 10 seceons.
    mark_onset      : Whether or not to draw vertical lines at the onset
                      of each detected vocalization. Default True.
    mark_offset     : Whether or not to draw vertical lines at the onffet
                      of each detected vocalization. Default True.

    '''
    colors = convert_annotation_codes()
    spec_fnames = glob(osp.join(spec_dir, '*.spect.npz'))
    predictions = pd.read_csv(annot_csv_path)
    plot_dur = int(plot_dur)

    if len(spec_fnames) == 0:
        raise FileNotFoundError(f'No spectrograms were found in {spec_dir}.\n',
                                f'Please check that {spec_dir} contains files ',
                                'ending with .spect.npz')

    if not osp.isdir(fig_dir):
        raise FileNotFoundError(f'The directory {fig_dir} does not exist.',
                                 ' Please create it.')

    for spec_fname in spec_fnames:

        tmp = np.load(spec_fname)
        S, f, t = tmp['s'], tmp['f'], tmp['t']

        name = spec_fname.split(osp.sep)[-1].rstrip('.spect.npz')
        rows = predictions[predictions['audio_path'] == name]

        # Make figures for plot_dur intervals.
        intervals = np.arange((t[-1] + 2 * plot_dur)//plot_dur) * plot_dur
        for t0, t1 in zip(intervals[:-1], intervals[1:]):

            fig = plt.figure(figsize=[18, 8])
            ax = fig.add_axes([0.05, 0.06, 0.93, 0.89])

            labeled = []
            t1 = min(t1, t[-1])
            if t0 < t[0]:
                i0 = 0
            else:
                i0 = ((t0 - t) >= 0.).nonzero()[0][0]

            i1 = ((t - t1) >= 0.).nonzero()[0][0]

            ax.imshow(S[:, i0:i1], aspect='auto', origin='upper',
                      extent=(t[i0], t[i1], f[0], f[-1]))

            ylim = ax.get_ylim()
            for row in rows.iterrows():
                onset_s, offset_s = row[1]['onset_s'], row[1]['offset_s']
                color = colors[row[1]['label']][2]
                label_hr = colors[row[1]['label']][0]

                if mark_onset:
                    ax.plot([onset_s, onset_s], ylim, '-', color='k', alpha=.2)
                if mark_offset:
                    ax.plot([offset_s, offset_s], ylim, '-', color='k', alpha=.2)

                rekt = Rectangle((onset_s, ylim[0]), offset_s-onset_s,
                                 300, facecolor=color, alpha=1., edgecolor=color)

                if label_hr not in labeled:
                    labeled.append(label_hr)
                    rekt.set_label(label_hr)

                ax.add_patch(rekt)

            ax.set_ylim(ylim)
            ax.set_xlim((t0, t1))
            ax.set_ylabel('Frequency (Hz)')
            ax.set_xlabel('Time (s)')
            ax.legend(loc='upper right')
            ax.set_title(f'Recording: {name.rstrip(".wav")} -- Interval: {t0} s to {t1} s')
            fname = f'{name.rstrip(".wav")}_{int(t0):04}s-{int(t1):04}s.png'               
            fig.savefig(osp.join(fig_dir, f'{plot_dur}s', fname))
            plt.close(fig)


parser = argparse.ArgumentParser()
parser.add_argument("annot_csv_path",
                    help=("relative or absolute path to the CSV ",
                          "file returned by 'vak predict predict.toml'."),
                    type=str)
parser.add_argument("spec_dir",
                    help=("The directory where the spectrograms returned ",
                          "by 'vak prep predict.toml' are stored."),
                    type=str)
parser.add_argument("fig_dir",
                    help=("The directory where to resulting PNG images ",
                          "will be stored."),
                        type=str)
parser.add_argument("--plot_dur",
                    help="Duration (in seconds) to plot in each figure.",
                    type=int,
                    default=10)
parser.add_argument("--mark_onsets",
                    help=("Whether or not to draw vertical lines at the \n",
                          "onset of each detected vocalization."),
                    action="store_true")
parser.add_argument("--mark_offsets",
                    help=("Whether or not to draw vertical lines at the \n",
                          "offset of each detected vocalization."),
                    action="store_true")
args = parser.parse_args()

plot_predictions(args.annot_csv_path, args.spec_dir, args.fig_dir,
                    args.plot_dur, args.mark_onsets, args.mark_offsets)
