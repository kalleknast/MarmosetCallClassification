# MarmosetCallClassification
Classification of marmoset vocalizations

The [model **link here**] gets 96% correct on the test set.

## Performance

Performance of the TweetyNet model trained on marmoset vocalizations*:

| Accuracy |	Levenshtein |	Loss	| Segment Error Rate |
|---------|-----------|------|-----|
| 0.9618	| 195.1 | 0.1217 | 0.3174 |

* Recorded and labeled by Daneil Y. Takahashi and colleauges

## Installation

 1. Install [vak](https://github.com/vocalpy/vak).
 2. Download the [model **link here**] and extract the ZIP archive.
 3. Set the paths in `predict_config.toml` to point to the model.


## Use
 1. Edit the configuration file `predict_config.toml` so that the paths point to the correct locations.
```
    [PREP]
    data_dir = "</path/to/the/WAV-files/to/run/the/model/on>"
    output_dir = "</path/to/where/the/organizing/CSV-file/should/be/stored>"
    spect_output_dir = "</path/to/where/the/spectrograms/should/be/stored>"
    [PREDICT]
    device = <"cpu" or "cuda">
    num_workers = <number of cpu threads used to load data>
    checkpoint_path = "</path/to/the/model/TweetyNet/checkpoints/max-val-acc-checkpoint.pt>"
    labelmap_path = "</path/to/the/model/labelmap.json>"
    spect_scaler_path = "</path/to/the/model/StandardizeSpect>"
    output_dir = "</dir/where/the/resulting/CSV-file/should/be/stored>"
    annot_csv_filename = "<name of the CSV-file with the predictions>.csv"
    csv_path = "</path/to/the/organizing/CSV-file/>.csv"
```
 2. Pre-process the WAV-files: `vak prep predict_config.toml`
 3. Predict: `vak predict predict_config.toml`. The resulting CSV file should be located and named according to `annot_csv_filename` above.
 4. (Optional) Plot the predictions for manual inspection: `python plot <annot_csv_filename> <spec_dir>`

