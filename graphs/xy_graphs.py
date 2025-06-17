#!/usr/bin/python3
import base64
import copy
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def remove_zeroes(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("Cannot make xy graph. Length of arrays not equal")

    for i in range(len(x_values) - 1, -1, -1):
        if y_values[i] == 0:
            del x_values[i]
            del y_values[i]

    return x_values, y_values

def make_xy_graph(display, x_values, y_values, x_label="", y_label="", title="", no_zeroes=False):
    if no_zeroes:
        remove_zeroes(x_values, y_values)

    fig, ax = plt.subplots()
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    if display == "line":
        ax.plot(x_values, y_values)
    elif display == "bar":
        if x_label == "Colour":
            bar_colours = copy.deepcopy(x_values)
            if bar_colours[0] == "colourless":
                bar_colours[0] = "sienna"
            ax.set_facecolor("lightgrey")
        else:
            bar_colours = None
        ax.bar(x_values, y_values, color=bar_colours)
    else:
        raise ValueError("No graph display specified (must be bar or line)")

    if y_label == "Win Rate":
        ax.set_ylim([0, 100])
        yticks = np.arange(0, 101, 20)
        ylabels = [f"{y}%" for y in yticks]
        ax.set_yticks(yticks, ylabels)

    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
    if title:
        ax.set_title(title)
    plt.tight_layout()

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='svg')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    return encoded
