#!/usr/bin/python3
import base64
import copy
import matplotlib.pyplot as plt
import numpy as np
import graphs.utils
from io import BytesIO

def make_xy_graph(display, x_values, y_values, x_label="", y_label="", title="", no_zeroes=False):
    if no_zeroes:
        x_values, y_values = graphs.utils.remove_zeroes(x_values, y_values)

    fig, ax = plt.subplots()
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    if display == "line":
        ax.plot(x_values, y_values)
        ax.scatter(x_values[:-1], y_values[:-1], marker=".")
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

    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
        if y_label == "Win Rate":
            ax.set_xlim([np.min(x_values), np.max(x_values)])
            ax.set_ylim([0, 100])
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            yticks = np.arange(0, 101, 12.5)
            ylabels = [f"{y}%" for y in yticks]
            ax.set_yticks(yticks, ylabels)
    if title:
        ax.set_title(title)
    plt.tight_layout()

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='svg')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    return encoded
