"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/stable/plugins/guides.html?#writers

Replace code below according to your needs.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

import numpy as np

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = tuple[DataType, dict, str]


def write_single_points_layer(path: str, data: Any, meta: dict) -> list[str]:
    """Writes a single points layer.

    Parameters
    ----------
    path : str
        A string path indicating where to save the image file.
    data : The layer data
        The `.data` attribute from the napari layer.
    meta : dict
        A dictionary containing all other attributes from the napari layer
        (excluding the `.data` layer attribute).

    Returns
    -------
    [path] : A list containing the string path to the saved file.
    """

    np.savetxt(path, data)
    # return path to any file(s) that were successfully written
    return [path]


def write_multiple(path: str, data: list[FullLayerData]) -> list[str]:
    """Writes multiple layers of different types.

    Parameters
    ----------
    path : str
        A string path indicating where to save the data file(s).
    data : A list of layer tuples.
        Tuples contain three elements: (data, meta, layer_type)
        `data` is the layer data
        `meta` is a dictionary containing all other metadata attributes
        from the napari layer (excluding the `.data` layer attribute).
        `layer_type` is a string, eg: "image", "labels", "surface", etc.

    Returns
    -------
    [path] : A list containing (potentially multiple) string paths to the saved file(s).
    """
    path = Path(path)
    output_paths = []
    for layer in data:
        if layer[-1] == "points":
            layer_name = layer[1]["name"]
            output_path = path.with_name(path.stem + "-" + layer_name + ".xyz")
            write_single_points_layer(output_path, layer[0], meta={})
            output_paths.append(str(output_path))
    # return path to any file(s) that were successfully written
    return output_paths
