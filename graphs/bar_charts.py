#!/usr/bin/python3
import matplotlib.pyplot as plt

def make_bar_chart(x_values, y_values, x_label = "", y_label="", title=""):
    fig, ax = plt.subplots()
    ax.bar(x_values, y_values)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
    if title:
        ax.set_title(title)
    plt.savefig("test_bar.png")
