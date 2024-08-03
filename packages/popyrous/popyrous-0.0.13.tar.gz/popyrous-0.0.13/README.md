# Popyrous

(Pouya's Python Routines) A collection of useful and frequently encountered Python routines for (data) science, research, development, and everyday life.

Author: Pouya P. Niaz (<pniaz20@ku.edu.tr> , <pouya.p.niaz@gmail.com>)  
Version: 0.0.13  
Last Update: August 02, 2024

This is a collection of Python routines for the following purposes:

- Checking for packages and installing missing ones iwithin scripts without the need for Jupyter and symbols like "!" and "%".
- Reading and writing `.mat` files coming to/from MathWorks MATLAB software.
- Building and manipulating time series data using sliding windows, low-pass filtering, etc.
- Building flexible and easy-to-use datasets for data analysis or machine learning out of structured time series experiments (multiple subjects, conditions, repetitions, etc.).
- Downloading data/files from the internet and Google Drive, using simple functions.
- Compressing or extracting Zip files with LZMA, etc., using simple functions.

Install with:

```bash
pip install popyrous
```

-------------------------------------------------------------

## 1- Intro

This package is a collection of routines I have widely used in my scientific, academic and engineering life.
It holds functionality for data and file manipulation, some tools for manipulating time series data,
some tools for extracting machine-learning-ready time series datasets from tabular timeseries data of structured experiments,
i.e., experiments performed with multiple subjects, under multiple conditions, with many repetitions, and so forth.

The contents and applications of this package are described briefly below. However, extensive documentation is provided in the docstrings of
all functions and classes in the code, which is where you should look for further information.

-------------------------------------------------------------

## 2- Contents and Submodules

### 2-1- matlab

This submodule contains functions for reading and writing data to and from `.mat` files.

- `type_compatible(typ)`: Determining whether or not a Python data type is compatible for writing into `.mat` files.
- `save_workspace(filename, masterdict)`: Save dictionary holding variables and data into `.mat` file.
- `load_workspace(filename, dictname)`: Load contents of `.mat` file into an (existing or new) dictionary.

### 2-2- packages

This submodule contains functions for checking which packages are installed in the environment without having to be in a notebook and running commands with `!` or `%`.
Also, you can check for a list of required packages (with or without required versions) and install missing packages, or wrong-versioned packages at the same time.

- `get_package_list()`: Get list (dictionary with keys being packages and values being versions) of packages in the (conda) environment.
- `check_packages(pkglst, install_missing, **kwargs)`: Get a list of required packages and see if they are all installed, installing the missing ones in the process.

Example:

```python
from popyrous.packages import check_packages
check_packages(["numpy","scipy","pandas==1.5.2"], install_missing=True, reinstall_wrong_versions=True)
```

### 2-3- timeseries

This submodule contains some classes and functions for working easily and efficiently with time series data.
You can filter data, pass it through sliding window and extract data for machine/deep learning, etc.
Also, given the dataframe of a tructured time series experiment where multiple subjects repeated an experiment
multiple times under various conditions, you can get their data, preprocess, post-process, filter, extract sliding window, etc.
and then keep some subjects, conditions, or trials for training and the rest for testing (for data analysis or machine learning), and so forth.

#### 2-3-1- sliding_window

The `sliding_window` function gets tabular timeseries data, extracts sliding windows from it, then downsamples or inverts them, etc. then returns them.
Sliding windows of time series data is used for time series modeling, prediction, classification, regression and forecasting problems.

#### 2-3-2- datasets

- `TabularDataset`: A class for reading time series data from an array, downsampling, preprocessing, and extracting sliding windows from it.
- `make_squeezed_dataset(hparams, inputs, outputs, **kwargs)`: Gets inputs/outputs, returns squeezed (2D) sliding window dataset ready to be fed to, e.g., an ANN model.
- `make_unsqueezed_dataset(hparams, inputs, outputs, **kwargs)`: Gets inputs/outputs, returns unsqueezed (3D) sliding window dataset ready to be fed to, e.g., an LSTM model.

#### 2-3-3- experiment

- `TimeseriesExperiment`: A class that gets a single dataframe containing the time series data of a series of structured experiments where
  there are multiple subjects, repetitions and trials. The data can then be processed such that data of each trial is separated and processed individually,
  some subjects, conditions or trials are kept for training/testing, there is preprocessing before extracting sliding windows, and postprocessing after it,
  and so on. This class comes in handy when the data of such a structured series of experiments needs to be processed and fed to a machine learning model, for instance.
- `generate_cell_array`: A function, which is a more concise version of the above class, doing everything in one shot and returning everything together.

#### 2-3-4- filt

Some functions for low-pass filtering time series data.

- `butter_lowpass_filter_forward` filters input data with a digital Butterworth low-pass filter gvien sampling and cutoff frequncies, and filter order.
  This filter is causal, and only goes forward in time. It does not see its future. It is used for real-time implementations.
  Because this filter is causal, it induces a phase shift, so the filtered signal will have a delay relative to the real signal.
  The lower the cutoff frequency, the longer the delay. This function in turn uses the `sosfiltfilt` utility of SciPy.
- `butter_lowpass_filter_back_to_back` filters input data similarly, but uses `sosfiltfilt` to go back to back, so it looks both to past and future.
  It can only smooth the data offline, since it has access to the future as well. Unlike the previous causal filter, it has no phase shift.
- `butter_highpass_filter_forward` and `butter_highpass_filter_back_to_back` can be used for similar purposes.
- The new `butter_filter` function encompasses virtually any kind of digital Butterworth filter, including all of the above.

#### 2-3-5- metrics

Some metrics used for time-series classification, etc.

- `tsc_metrics`: Time-series classification metrics, including accuracy, f1 score, concurrency (transitioning on time) and consistency (not changing prediction in consistent non-transitioning portions of the data)

#### 2-3-6- cwt

Continmuous Wavelet Transform

- `cwt_for_batch`: gets a numpy array of shape, e.g., (batchsize, channels, seqlen) [could be any shape, as long as time is the last dimension]
  and returns an array of its CWT coefficients.
  Additionally, it can downsample it and remove the last row and column. Returns a (batchsize, channels, coefs, seqlen) dataset of 2D images.
- `cwt_for_tensor`: gets a data tensor of any shape and simply performs CWT on it. Takes the last dimension as time, and adds a dimension
  to the beginning, containing coefficients.

### 2-4- web

This submodule contains some web-related functions for downloading files from the internet or Google Drive, storing them, reading their contents, etc.

- `download_google_drive_file(shareable_link, output_file)`: Gets shareable link of a Google Drive file, and downlaods it.
- `download(url, filename, **kwargs)`: Downlaods material from the internet, and reads its content or stores in a file.

### 2-5- zipfiles

This submodule contains some functions for compressing/decompressing zip files.

- `extract_files(fileName)`: Extracts everything in the zip file.
- `compress_files(file_name, **kwargs)`: Compresses files into a zip file. Options for compression method, etc. are provided.

### 2-6- ml

This submodule contains some machine-learning-related code. For now, it just contains a function for pretty plotting confusion matrices (see credits).

- `make_confusion_matrix` gets a confusion matrix and some parameters, and pretty plots it.

-------------------------------------------------------------

## 3- License

This package is built with MIT license.

-------------------------------------------------------------

## 4- Credits

Pretty plotting confusion matrix:  
Dennis T  
<https://github.com/DTrimarchi10/confusion_matrix>  
<https://medium.com/@dtuk81/confusion-matrix-visualization-fc31e3f30fea>
