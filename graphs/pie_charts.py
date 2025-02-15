#!/usr/bin/python3
import base64
import matplotlib.pyplot as plt
from io import BytesIO

def make_pie_chart(labels, values, title=""):
    # remove zero values from data
    labels, values = (list(i) for i in zip(*filter(all, zip(labels, values))))

    # sort by descending value
    labels = [label for _, label in sorted(zip(values, labels))]
    values = sorted(values)

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct=lambda pct: int(round(pct*sum(values)/100.0)))
    if title:
        ax.set_title(title)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    return encoded
