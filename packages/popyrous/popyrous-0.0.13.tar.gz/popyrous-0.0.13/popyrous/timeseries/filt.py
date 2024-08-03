
import numpy as np
from scipy.signal import butter, sosfilt, sosfiltfilt
import warnings


def butter_lowpass_filter_back_to_back(data, cutoff, fs, order, axis=-1, padtype='odd', padlen=None):
    """Low-pass filter the given data back-to-back (using `sosfiltfilt`) using a Butterworth filter.

    ### Args:
        `data` (numpy array): Data, where each column is a timeseries, and each row is a time step.
        `cutoff` (float): Cutoff frequency, Hz
        `fs` (float): Sampling frequency, Hz
        `order` (int): Order of the filter
        `axis` (int): Axis along which to filter. Defaults to -1.
        `padtype` (str): Type of padding to use. Defaults to 'odd'. Must be 'odd', 'even', 'constant', or None.
        `padlen` (int): Number of samples to pad. Defaults to None.

    ### Returns:
        Filtered Data
    """
    warnings.warn("This function is depracated. Use `butter_filter` instead.", DeprecationWarning)
    sos = butter(order, cutoff, btype='lowpass', fs=fs, analog=False, output='sos')
    y = sosfiltfilt(sos, data, axis=axis, padtype=padtype, padlen=padlen)
    return y




def butter_lowpass_filter_forward(data, cutoff, fs, order, axis=-1, zi=None):
    """Low-pass filter the given data by only moving forwards (using `sosfilt`, not `sosfiltfilt`) using a Butterworth filter.

    ### Args:
    
        `data` (numpy array): Data, where each column is a timeseries, and each row is a time step.
        `cutoff` (float): Cutoff frequency, Hz
        `fs` (float): Sampling frequency, Hz
        `order` (int): Order of the filter
        `axis` (int): Axis along which to filter. Defaults to -1.
        `zi` (array): Initial conditions for the filter. Defaults to None.

    ### Returns:
        Filtered Data, if `zi` is None. Otherwise, (Filtered Data, Final Conditions `zf`)
    """
    warnings.warn("This function is depracated. Use `butter_filter` instead.", DeprecationWarning)
    sos = butter(order, cutoff, btype='lowpass', analog=False, fs=fs, output='sos')
    y = sosfilt(sos, data, axis=axis, zi=zi)
    return y



def butter_highpass_filter_back_to_back(data, cutoff, fs, order, axis=-1, padtype='odd', padlen=None):
    """High-pass filter the given data back-to-back (using filtfilt) using a Butterworth filter.

    ### Args:
        `data` (numpy array): Data, where each column is a timeseries, and each row is a time step.
        `cutoff` (float): Cutoff frequency, Hz
        `fs` (float): Sampling frequency, Hz
        `order` (int): Order of the filter
        `axis` (int): Axis along which to filter. Defaults to -1.
        `padtype` (str): Type of padding to use. Defaults to 'odd'. Must be 'odd', 'even', 'constant', or None.
        `padlen` (int): Number of samples to pad. Defaults to None.

    ### Returns:
        Filtered Data
    """
    warnings.warn("This function is depracated. Use `butter_filter` instead.", DeprecationWarning)
    sos = butter(order, cutoff, btype='highpass', analog=False, fs=fs, output='sos')
    y = sosfiltfilt(sos, data, axis=axis, padtype=padtype, padlen=padlen)
    return y




def butter_highpass_filter_forward(data, cutoff, fs, order, axis=-1, zi=None):
    """High-pass filter the given data by only moving forwards (using filt, not filtfilt) using a Butterworth filter.

    ### Args:
        `data` (numpy array): Data, where each column is a timeseries, and each row is a time step.
        `cutoff` (float): Cutoff frequency, Hz
        `fs` (float): Sampling frequency, Hz
        `order` (int): Order of the filter
        `axis` (int): Axis along which to filter. Defaults to -1.
        `zi` (array): Initial conditions for the filter. Defaults to None.

    ### Returns:
        Filtered Data
    """
    warnings.warn("This function is depracated. Use `butter_filter` instead.", DeprecationWarning)
    sos = butter(order, cutoff, btype='highpass', analog=False, fs=fs, output='sos')
    y = sosfilt(sos, data, axis=axis, zi=zi)
    return y




def butter_filter(data, freqs, fs, order, btype='lowpass', back_to_back=False, axis=-1, filt_kwargs={}):
    """Filter the given data using a Butterworth filter.

    ### Args:
    
        - `data` (numpy array): Data, where each column is a timeseries, and each row is a time step.
        - `freqs` (float): Cutoff frequency (highpass and lowpass), or list of cutoff frequencies (bandpass and bandstop), Hz
        - `fs` (float): Sampling frequency, Hz
        - `order` (int): Order of the filter
        - `btype` (str): Type of filter (`lowpass`, `highpass`, `bandpass`, `bandstop`)
        - `back_to_back` (bool): Whether to use `sosfiltfilt` or `sosfilt`. Defaults to False.
        - `axis` (int): Axis along which to filter. Defaults to -1.
        - `filt_kwargs` (dict): Additional arguments to pass to the `sosfiltfilt` or `sosfilt` function.
            - The `sosfilt` function takes another optional argument `zi`, which is the initial conditions for the filter.
            - The `sosfiltfilt` function takes two optional arguments `padtype` and `padlen`, which are the type of padding to use and the number of
              samples to pad, respectively.
          

    ### Returns:
    
        - Filtered Data, if it were a back_to_back filter.
        - Filtered Data, if it were a forward filter and `zi` were not provided.
        - (Filtered Data, Final Conditions `zf`), if it were a forward filter and `zi` were provided.
    """
    sos = butter(order, freqs, btype=btype, analog=False, fs=fs, output='sos')
    if back_to_back:
        y = sosfiltfilt(sos, data, axis=axis, **filt_kwargs)
    else:
        y = sosfilt(sos, data, axis=axis, **filt_kwargs)
    return y