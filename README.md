# MarmosetCallClassification
Classification of marmoset vocalizations

The [model](https://snapassamusay.files.wordpress.com/2023/01/model.zip) gets 96% correct on the test set.

## Performance

Performance of the TweetyNet model trained on marmoset vocalizations*:

| Accuracy |	Levenshtein |	Loss	| Segment Error Rate |
|---------|-----------|------|-----|
| 0.9618	| 195.1 | 0.1217 | 0.3174 |

* Recorded and labeled by Daniel Y. Takahashi and colleauges. See [Takahashi, D. Y., Fenley, A. R., Teramoto, Y., Narayanan, D. Z., Borjon, J. I., Holmes, P., & Ghazanfar, A. A. (2015). The developmental dynamics of marmoset monkey vocal production. Science, 349(6249), 734-738.](http://www.princeton.edu/~dtakahas/publications/Takahashi%20et%20al%202015%20Developmental%20dynamics%20vocalization) for details.

## Installation

 1. Install [vak](https://github.com/vocalpy/vak).
 2. Download the [model](https://snapassamusay.files.wordpress.com/2023/01/model.zip) and extract the ZIP archive.
 

## Use
 1. Prepare directories and the configuration file. Either by creating the directories (relative to your working directory) in `predict_example.toml` (`data/WAV`, `data/preprocessed` and `results/predictions`), or by editing the configuration file `predict.toml` so that the paths point to the correct locations.
```toml
    [PREP]
    data_dir = "</path/to/the/WAV-files/to/run/the/model/on>"
    output_dir = "</path/to/where/the/organizing/CSV-file/should/be/stored>"
    spect_output_dir = "</path/to/where/the/spectrograms/should/be/stored>"
    [PREDICT]
    device = '<"cpu" or "cuda">'
    checkpoint_path = "</path/to/the/model/>TweetyNet/checkpoints/max-val-acc-checkpoint.pt"
    labelmap_path = "</path/to/the/model/>labelmap.json"
    spect_scaler_path = "</path/to/the/model/>StandardizeSpect"
    output_dir = "</dir/where/the/resulting/CSV-file/should/be/stored>"
    annot_csv_filename = "<name of the CSV-file with the predictions>.csv"
```
 2. Pre-process the WAV-files: `vak prep predict.toml`
 3. Predict: `vak predict predict.toml`. The resulting CSV file should be located and named according to `annot_csv_filename` above.
 4. (Optional) Plot the predictions for manual inspection: 
    ```terminal
    python3 plot.py <annot_csv_filename> <spec_dir> <fig_dir> --plot_dur 10 --mark_onsets --mark_offsets
    ```

