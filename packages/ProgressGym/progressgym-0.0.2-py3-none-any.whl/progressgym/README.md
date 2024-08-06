# ProgressAlign: Dataset & Experimental Framework for Progress-Aware Alignment

## Building the dataset

- Running `python ./build_dataset.py` will automatically download the relevant files and then compile them into the desired dataset. Specifically, it will...
  - Download and decompress raw data files from multiple sources, placing them in `./dataset/raw_downloads` 
  - Organize downloaded data into an unified format, and the resulting historical text dataset is saved as a series of files `./dataset/dataset_textseq/[century_num]/[year_num].json` 
  - Train a series of historical language models  `./dataset/dataset_modelseq/[century_num]` using the historical text dataset.



## Running the benchmark

- Running `python ./run_benchmark.py --challenge [challenge_name] --testtaker [path_to_tested_system]` will produce the benchmark results. Omitting `--challenge [challenge_name]` will default to testing all challenges.

