#!/usr/bin/python3
import matplotlib.pyplot as plt

def make_pie_chart(labels, values):
    labels = [labels for _, labels in sorted(zip(values, labels))]
    values = sorted(values)

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct=lambda pct: int(round(pct*sum(values)/100.0)))
    plt.savefig("test_pie.png")
