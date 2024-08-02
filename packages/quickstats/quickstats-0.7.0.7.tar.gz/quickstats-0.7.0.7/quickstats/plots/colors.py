from typing import List, Dict, Optional, Union

from cycler import cycler
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import (
    to_rgba, get_named_colors_mapping,
    ListedColormap, LinearSegmentedColormap
)
#from matplotlib.colormaps import register
#from matplotlib.cm import get_cmap as gcm

def get_cmap(source: Union[List[str], str, ListedColormap, LinearSegmentedColormap], 
             size: Optional[int] = None) -> ListedColormap:
    """
    Get a Matplotlib colormap from a name, list of colors, or an existing colormap.
    
    Parameters
    ----------
    source : Union[List[str], str, ListedColormap, LinearSegmentedColormap]
        The source for the colormap. It can be:
        - A string name of the colormap.
        - A list of color strings.
        - An existing colormap instance (ListedColormap or LinearSegmentedColormap).
    size : Optional[int], default: None
        The number of entries in the colormap lookup table. If None, the original size is used.
    
    Returns
    -------
    ListedColormap
        A Matplotlib colormap.
    
    Raises
    ------
    ValueError
        If `source` is not a recognized type.
        
    Example
    -------
    >>> get_cmap('viridis', size=10)
    >>> get_cmap(['#FF0000', '#00FF00', '#0000FF'], size=5)
    >>> get_cmap(mpl.colormaps['viridis'], size=256)
    """
    if isinstance(source, str):
        cmap = mpl.colormaps.get_cmap(source)
    elif isinstance(source, (ListedColormap, LinearSegmentedColormap)):
        cmap = source.copy()
    elif isinstance(source, list):
        cmap = ListedColormap(source)
    else:
        raise ValueError(f"Invalid source type for colormap: {type(source)}")
    if size is not None:
        return cmap.resampled(size)
    return cmap

def get_cmap_rgba(source: Union[List[str], str, ListedColormap, LinearSegmentedColormap], 
                  size: Optional[int] = None) -> np.ndarray:
    """
    Retrieve the RGBA values from a colormap.
    
    Parameters
    ----------
    source : Union[List[str], str, ListedColormap, LinearSegmentedColormap]
        The source for the colormap. It can be:
        - A string name of the colormap.
        - A list of color strings.
        - An existing colormap instance (ListedColormap or LinearSegmentedColormap).
    size : Optional[int], default: None
        The number of entries in the colormap lookup table. If None, the original size is used.
    
    Returns
    -------
    np.ndarray
        An array of RGBA values.
        
    Example
    -------
    >>> get_cmap_rgba('viridis', size=10)
    array([[0.267004, 0.004874, 0.329415, 1.      ],
           [0.282623, 0.140926, 0.457517, 1.      ],
           ...,
           [0.993248, 0.906157, 0.143936, 1.      ]])
    >>> get_cmap_rgba(['#FF0000', '#00FF00', '#0000FF'], size=5)
    array([[1.        , 0.        , 0.        , 1.        ],
           [0.75      , 0.5       , 0.25      , 1.        ],
           [0.5       , 1.        , 0.5       , 1.        ],
           [0.25      , 0.75      , 0.75      , 1.        ],
           [0.        , 0.        , 1.        , 1.        ]])
    >>> get_cmap_rgba(mpl.colormaps['plasma'], size=256)
    """
    cmap = get_cmap(source, size=size)
    
    # Ensure cmap.N is used to retrieve correct number of colors
    rgba_values = cmap(np.linspace(0, 1, cmap.N))
    
    return rgba_values

def get_cmap_rgba(source:Optional[Union[List, str]], size:Optional[int]=None) -> List[List[float]]:
    cmap = get_cmap(source, size=size)
    return cmap(range(cmap.N))
    
def get_rgba(color: str, alpha: float = 1.0) -> List[float]:
    """
    Convert a color string to an RGBA list with a specified alpha value.
    
    Parameters
    ----------
    color : str
        A color string (e.g., 'blue', '#00FF00', 'rgb(255,0,0)', etc.).
    alpha : float, default: 1.0
        The alpha (transparency) value to set, in the range [0.0, 1.0].
        
    Returns
    -------
    List[float]
        A list of RGBA components [R, G, B, A] with the specified alpha value.
    
    Example
    -------
    >>> get_rgba('blue', alpha=0.5)
    [0.0, 0.0, 1.0, 0.5]
    >>> get_rgba('#FF5733', alpha=0.8)
    [1.0, 0.3411764705882353, 0.2, 0.8]
    """
    rgba = list(to_rgba(color))
    rgba[-1] = alpha
    return rgba

def validate_color(color: str) -> None:
    """
    Validate a color string by converting it to RGBA.
    
    Parameters
    ----------
    color : str
        The color string to validate.
        
    Raises
    ------
    ValueError
        If the color cannot be converted to RGBA.
    """
    try:
        to_rgba(color)
    except ValueError:
        raise ValueError(f"Invalid color value: {color}")
        
def register_colors(colors: Dict[str, Union[str, Dict[str, str]]]) -> None:
    """
    Register colors to matplotlib's color registry.
    
    Parameters
    ----------
    colors : Dict[str, Union[str, Dict[str, str]]]
        A dictionary where keys are color labels and values are either color strings or 
        dictionaries mapping sub-labels to color strings.
        
    Raises
    ------
    ValueError
        If any of the colors cannot be converted to RGBA.
    TypeError
        If the color values are neither strings nor dictionaries.
    
    Example
    -------
    >>> register_colors({
    ...     'primary': '#FF0000',
    ...     'secondary': {'shade1': '#00FF00', 'shade2': '#0000FF'}
    ... })
    """
    grouped_colors = {}

    for label, color in colors.items():
        if isinstance(color, dict):
            for sublabel, subcolor in color.items():
                validate_color(subcolor)
                full_label = f'{label}:{sublabel}'
                grouped_colors[full_label] = subcolor
        elif isinstance(color, str):
            validate_color(color)
            grouped_colors[label] = color
        else:
            raise TypeError(f"Color for '{label}' must be a string or a dictionary.")
    
    # Extend the named colors dictionary
    named_colors = get_named_colors_mapping()
    named_colors.update(grouped_colors)

def register_cmaps(listed_colors:Dict[str, List[str]], force:bool=True) -> None:
    """
    Register listed color maps to the matplotlib registry.
    
    Parameters
    ----------
    listed_colors : Dict[str, List[str]]
        A dictionary mapping from color map name to the underlying list of colors.
        
    Example
    -------
    >>> register_cmaps({'my_cmap': ['#FF0000', '#00FF00', '#0000FF']})
    """
    for name, colors in listed_colors.items():
        cmap = ListedColormap(colors, name=name)
        mpl.colormaps.register(name=name, cmap=cmap, force=force)

def get_color_cycle(source: Union[List[str], str, ListedColormap]) -> cycler:
    """
    Convert a color source to a Matplotlib cycler object.
    
    Parameters
    ----------
    source : Union[List[str], str, ListedColormap]
        The source of colors. It can be:
        - A list of color strings.
        - A string name of the colormap.
        - A `ListedColormap` instance.
        
    Returns
    -------
    cycler
        A cycler object containing colors from the source.
    
    Example
    -------
    >>> get_color_cycle(['#FF0000', '#00FF00', '#0000FF'])
    >>> get_color_cycle('viridis')
    >>> get_color_cycle(mpl.colormaps['viridis'])
    """
    if isinstance(source, str):
        cmap = get_cmap(source)
        colors = cmap.colors
    elif isinstance(source, ListedColormap):
        colors = source.colors
    elif isinstance(source, list):
        colors = source
    else:
        raise ValueError(f"Invalid source type for colors: {type(source)}")
    return cycler(color=colors)

# taken from https://matplotlib.org/stable/tutorials/colors/colormaps.html
def plot_color_gradients(cmap_list: List[str], size: Optional[int] = None) -> None:
    """
    Plot a series of color gradients for the given list of colormap names.
    
    Parameters
    ----------
    cmap_list : List[str]
        List of colormap names.
    size : Optional[int], default: None
        The colormap will be resampled to have `size` entries in the lookup table.
        
    Example
    -------
    >>> plot_color_gradients(['viridis', 'plasma', 'inferno', 'magma', 'cividis'])
    >>> plot_color_gradients(['Blues', 'Greens', 'Reds'], size=128)
    """
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    # Calculate the figure height based on the number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows, figsize=(6.4, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                        left=0.2, right=0.99, hspace=0.4)

    # Plot each colormap gradient
    for ax, name in zip(axs, cmap_list):
        cmap = get_cmap(name, size=size)
        ax.imshow(gradient, aspect='auto', cmap=cmap)
        ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)
        ax.set_axis_off()