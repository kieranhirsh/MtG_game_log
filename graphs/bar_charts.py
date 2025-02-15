#!/usr/bin/python3
import base64
import matplotlib.pyplot as plt
from io import BytesIO

def make_bar_chart(x_values, y_values, x_label = "", y_label="", title=""):
    fig, ax = plt.subplots()
    ax.bar(x_values, y_values)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
    if title:
        ax.set_title(title)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    return encoded
