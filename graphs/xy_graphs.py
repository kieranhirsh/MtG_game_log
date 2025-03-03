#!/usr/bin/python3
import base64
import matplotlib.pyplot as plt
from io import BytesIO

def make_xy_graph(display, x_values, y_values, x_label="", y_label="", title=""):
    fig, ax = plt.subplots()
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    if display == "line":
        ax.plot(x_values, y_values)
    elif display == "bar":
        if x_label == "Colour":
            bar_colours = x_values
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
    if title:
        ax.set_title(title)
    plt.tight_layout()

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='svg')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    return encoded
