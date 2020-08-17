import matplotlib.pyplot as plt
import numpy as np


def merge_dicts(dicts_in):
    """
    Concatenates contents of a list of N state dicts into a single dict by
    prepending a new dimension of size N. This is more convenient for plotting
    and analysis. Requires dicts to have consistent keys and have values that
    are numpy arrays.
    """
    dict_out = {}
    for k in dicts_in[0].keys():
        dict_out[k] = []
        for d in dicts_in:
            dict_out[k].append(d[k])
        dict_out[k] = np.array(dict_out[k])
    return dict_out


# TODO bullet proof error handling
def plot(x, y1, y2=None, xlabel="", ylabels=["", ""]):
    """
    Plot - a function to quickly create good looking plots

    Inputs
        x, an array of length N representing the x coordinates
        y1, an array of size (N, m) representing the y coordinates of m functions
        y2, an array of size (N, m) representing the y coordinates of m functions, plotted on second set of axes
            defaults to None in which case only one set of axes is used
        xlabel, a string to label the x axis of the plots, defaults to an empty string
        ylabels, an array of length 2 with each element being the y axis label for the y1 and y2 axes respectively

    Outputs
        fig, a matplotlib figure handle
    """
    y1 = np.array(y1, ndmin=2)
    if y2 is None:
        (fig, axes) = plt.subplots(nrows=1, ncols=1, sharex=True, num='State vs Time')
        ax = axes
        [ax.plot(x, y1[i, :]) for i in range(len(y1))]
        ax.set(xlabel='Time (s)', ylabel=ylabels[0])
    else:
        y2 = np.array(y2, ndmin=2)
        (fig, axes) = plt.subplots(nrows=2, ncols=1, sharex=True, num='State vs Time')
        ax = axes[0]
        [ax.plot(x, y1[i, :]) for i in range(len(y1))]
        ax.set(xlabel=xlabel, ylabel=ylabels[0])
        ax.grid()
        ax = axes[1]
        [ax.plot(x, y2[i, :]) for i in range(len(y2))]
        ax.set(xlabel=xlabel, ylabel=ylabels[1])
    ax.grid()
    plt.show()
    return fig
