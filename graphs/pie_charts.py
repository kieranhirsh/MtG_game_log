from io import BytesIO
import re
import base64
import copy
import matplotlib.pyplot as plt

def make_pie_chart(labels, values, title=""):
    fig, ax = plt.subplots()

    # if we're binning by colour
    if re.match(r'^.*per Colour$', title):
        pie_colours = copy.deepcopy(labels)
        pie_colours[0] = "sienna"
        fig.patch.set_facecolor("lightgrey")
        pie_colours, values = (list(i) for i in zip(*filter(all, zip(pie_colours, values))))
        pie_colours = [pie_colour for _, pie_colour in sorted(zip(values, pie_colours))]
    else:
        pie_colours = None

    # remove zero values from data
    labels, values = (list(i) for i in zip(*filter(all, zip(labels, values))))

    # sort by descending value
    labels = [label for _, label in sorted(zip(values, labels))]
    values = sorted(values)

    # do the plotting
    patches, texts, autotexts = ax.pie(values, labels=labels, autopct=lambda pct: int(round(pct*sum(values)/100.0)), colors=pie_colours)

    # change the inner text colour if we're plotting vs colour
    if re.match(r'^.*per Colour$', title):
        for ii in range(len(pie_colours)):
            if pie_colours[ii] == "black":
                autotexts[ii].set_color("white")

    # add the title
    if title:
        ax.set_title(title)

    # encode so that html can display the graph
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='svg')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    return encoded
