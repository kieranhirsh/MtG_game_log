#!/usr/bin/python3
import base64
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def make_line_graph(x_values, y_values, x_label="", y_label="", title="", legend=[]):
    fig, ax = plt.subplots()
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    if len(x_values) != len(y_values):
        raise ValueError("make_line_graph: x_values and y_values must contain same number of sets of data")

    xmin = []
    xmax = []

    for i in range(len(x_values)):
        ax.plot(x_values[i], y_values[i], label=legend[i] if legend else None)
        ax.scatter(x_values[i][:-1], y_values[i][:-1], marker=".")
        xmin.append(np.min(x_values[i]))
        xmax.append(np.max(x_values[i]))

    if legend:
        ax.legend()

    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
        if y_label == "Win Rate":
            ax.set_xlim([np.min(xmin), np.max(xmax)])
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
