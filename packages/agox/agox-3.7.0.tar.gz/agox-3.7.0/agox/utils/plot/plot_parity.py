import numpy as np
from numpy.typing import NDArray
from typing import List, Dict

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from agox.utils.metrics import get_metrics


def get_limits(
    arrays: NDArray,
    extra: float = 0.0,
    extra_min: float = None,
    extra_max: float = None,
):
    max_value = -np.inf
    min_value = np.inf

    for arr in arrays:
        max_value = max(max_value, np.max(arr))
        min_value = min(min_value, np.min(arr))

    if extra_min is not None:
        min_value -= extra_min
    if extra_max is not None:
        max_value += extra_max

    max_value += extra
    min_value -= extra

    return [min_value, max_value]


def plot_parity(
    ax: Axes,
    truths: Dict[str, NDArray],
    predictions: Dict[str, NDArray],
    strict_keys=None,
    inset: bool = False,
    inset_kwargs: dict = None,
    limits_extra_max: float = 1.0,
    limits_extra_min: float = 1.0,
    metrics_used=None,
    scatter_kwargs=None,
):
    """
    Plot parity plot for a set of predictions and truths.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes to plot on.
    truths : Dict[str, NDArray]
        Dictionary with the true values.
    predictions : Dict[str, NDArray]
        Dictionary with the predicted values.
    strict_keys : List[str], optional
        List of keys to plot, if given only these keys will be plotted. If not,
        all pairs of keys in both truths and predictions will be plotted.
    inset : bool, optional
        Whether to plot an inset with the same data.
    inset_kwargs : dict, optional
        Kwargs to pass to the inset axes.
    limits_extra_max : float, optional
        Extra space to add to the limits of the plot.
    limits_extra_min : float, optional
        Extra space to add to the limits of the plot.
    metrics_used : List[str], optional
        List of metrics to display in the legend.
    scatter_kwargs : dict, optional
        Kwargs to pass to the scatter plot.
    """    


    base_scatter_kwargs = {
        "edgecolor": "white",
        "linewidth": 1,
        "alpha": 1.0,
        "s": 50,
    }

    if scatter_kwargs is not None:
        base_scatter_kwargs.update(scatter_kwargs)

    # Keys in both truths and preds
    keys = set(truths.keys()).intersection(set(predictions.keys()))

    if strict_keys is not None:
        keys = keys.intersection(strict_keys)

    for key in keys:
        true = truths[key]
        pred = predictions[key]

        metrics = get_metrics(true, pred)

        label = f"{key}"
        for metric in metrics_used:
            label += f"\n{metric.upper()}: {metrics[metric]:.2f}"

        l1 = ax.scatter(
            true,
            pred,
            **base_scatter_kwargs,
            label=label,
        )

    # Prettyness
    limits = get_limits(
        predictions.values(), extra_max=limits_extra_max, extra_min=limits_extra_min
    )
    ax.plot(limits, limits, color="black", linestyle="--")
    ax.set_xlim(limits)
    ax.set_ylim(limits)
    # Add inset in lower right side:
    if inset:
        default_inset_kwargs = {
            "width": "40%",
            "height": "40%",
            "loc": "lower right",
            "delta": 5,
        }
        default_inset_kwargs.update(inset_kwargs or {})
        inset_kwargs = default_inset_kwargs
        inset_delta = inset_kwargs.pop("delta")
        ax_inset = inset_axes(ax, **inset_kwargs)

        inset_predictions = {}
        inset_truths = {}
        inset_min = limits[0] + limits_extra_min
        inset_max = inset_min + inset_delta
        for key in predictions.keys():
            pred = predictions[key]
            true = truths[key]
            mask = (pred <= inset_max) * (true <= inset_max)
            inset_predictions[key] = pred[mask]
            inset_truths[key] = true[mask]

        plot_parity(
            ax_inset,
            inset_truths,
            inset_predictions,        
            inset=False,
            metrics_used=metrics_used,
            limits_extra_max=0,
            limits_extra_min=1,
        )
        ax_inset.legend(fontsize=7)
        ax_inset.set_xticklabels([])
        ax_inset.set_yticklabels([])

        limits = get_limits(inset_predictions.values(), extra_max=0, extra_min=1)

        # Plot the area of the inset in the main plot
        ax.add_patch(
            plt.Rectangle(
                (limits[0], limits[0]),
                limits[1] - limits[0],
                limits[1] - limits[0],
                fill=False,
                linestyle="--",
                color="black",
            )
        )

    ax.legend(loc="upper left")
