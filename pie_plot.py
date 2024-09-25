import matplotlib.pyplot as plt
from typing import Union, Tuple, Optional
from anndata import AnnData
import seaborn as sns
import pandas as pd
from dandelion import Dandelion

def piechart(
    vdj_data: Union[AnnData, Dandelion],
    color: str,
    figsize: Tuple[Union[int, float], Union[int, float]] = (8, 8),
    title: Optional[str] = None,
    min_clone_size: int = 1,
    clone_key: Optional[str] = None,
    threshold: float = 0.05,  # Threshold for grouping into "Other"
    **kwargs,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    A pie chart function to plot usage of V/J genes in the data.

    Parameters
    ----------
    vdj_data : Union[AnnData, Dandelion]
        `Dandelion` or `AnnData` object.
    color : str
        column name in metadata for plotting in pie chart.
    figsize : Tuple[Union[int, float], Union[int, float]], optional
        figure size.
    title : Optional[str], optional
        title of plot.
    min_clone_size : int, optional
        minimum clone size to keep.
    clone_key : Optional[str], optional
        column name for clones. None defaults to 'clone_id'.
    threshold : float, optional
        minimum percentage for a category to be shown individually.
        Categories below this threshold will be grouped into "Other".
    **kwargs
        passed to `plt.pie`.

    Returns
    -------
    Tuple[plt.Figure, plt.Axes]
        pie chart.
    """
    if isinstance(vdj_data, Dandelion):
        data = vdj_data.metadata.copy()
    elif isinstance(vdj_data, AnnData):
        data = vdj_data.obs.copy()

    min_size = min_clone_size

    if clone_key is None:
        clone_ = "clone_id"
    else:
        clone_ = clone_key

    size = data[clone_].value_counts()
    keep = list(size[size >= min_size].index)
    data_ = data[data[clone_].isin(keep)]

    counts = data_[color].value_counts(normalize=True)

    # Apply the threshold
    counts_above_threshold = counts[counts >= threshold]
    counts_below_threshold = counts[counts < threshold]

    if not counts_below_threshold.empty:
        counts_above_threshold['Other'] = counts_below_threshold.sum()

    # Initialize the matplotlib figure
    fig, ax = plt.subplots(figsize=figsize)

    # plot
    ax.pie(counts_above_threshold, labels=counts_above_threshold.index, autopct='%1.1f%%', **kwargs)

    if title is None:
        ax.set_title(color.replace("_", " ") + " usage")
    else:
        ax.set_title(title)

    # Set aspect ratio to be equal so that pie is drawn as a circle
    ax.axis('equal')

    return fig, ax
