import io
import base64

from flask import make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def makePlotFigure(
        straces,
        slabels=[],
        title="",
        xlabel="",
        ylabel="",
        ylines=[]
):
    """
    Given a list of satistic traces, create a plot of them.
    """
    fig = Figure(tight_layout=True, figsize=(10, 6))

    ax = fig.add_subplot(1, 1, 1)

    for i in range(0, len(straces)):
        s = straces[i]

        l = ""
        if (slabels != []):
            l = (slabels[i])

        ax.plot(s, linewidth=0.15, label=l)

        if (xlabel and xlabel != ""):
            ax.set_xlabel(xlabel)

        if (ylabel and ylabel != ""):
            ax.set_ylabel(ylabel)

    for y in ylines:
        ax.axhline(y=y, xmin=0.0, xmax=1.0, color='r')

    if (title and title != ""):
        fig.suptitle(title, y=1.0)

    handles, labels = ax.get_legend_handles_labels()
    lg = ax.legend(
        handles,
        labels,
        loc="lower left",
        bbox_to_anchor=(0.0, 1.01),
        ncol=1
    )

    return fig


def b64_plot_png(figure):
    """
    Return a Flask response object containing the rendered image.
    """
    sio = io.BytesIO()

    canvas = FigureCanvas(figure)

    canvas.print_png(sio)

    return base64.encodebytes(sio.getvalue()).decode('ascii')
