from typing import Optional, Union, Tuple

import numpy as np

from quickstats.core.typing import ArrayLike
from quickstats.maths.statistics import bin_edge_to_bin_center

class Binning:
    """
    A class for defining binning information.

    Parameters
    ----------
    bins : ArrayLike or int
        If ArrayLike, specifies the bin edges directly. 
        If int, specifies the number of bins, in which case `bin_range` must be provided.
    bin_range : Optional[ArrayLike], optional
        The range of the bins as a tuple (low, high), required if `bins` is an int.

    Attributes
    ----------
    bin_edges : np.ndarray
        The edges of the bins.
    bin_centers : np.ndarray
        The centers of the bins.
    bin_widths : np.ndarray
        The widths of the bins.
    nbins : int
        The number of bins.

    Methods
    -------
    bin_edges
        Returns the edges of the bins.
    bin_centers
        Returns the centers of the bins.
    bin_widths
        Returns the widths of the bins.
    nbins
        Returns the number of bins.
    """
    
    def __init__(self, bins: Union[ArrayLike, int], bin_range: Optional[ArrayLike] = None):
        if np.ndim(bins) == 1:
            if len(bins) < 2:
                raise ValueError('Number of bin edges must be greater than 1 to define a binning.')
            self._bin_edges = np.array(bins)
        elif np.ndim(bins) == 0:
            if (not isinstance(bins, int)) or (bins < 1):
                raise ValueError('Number of bins must be greater than 0 to define a binning.')
            if bin_range is None:
                raise ValueError('`bin_range` must be given when `bins` is a number.')
            bin_low, bin_high = bin_range
            if bin_low > bin_high:
                raise ValueError('`bin_range[0]` can not be larger than `bin_range[1]`.')
            self._bin_edges = np.linspace(bin_low, bin_high, bins + 1)
        else:
            raise ValueError('Invalid value for `bins`. It must be either an array representing the bin edges or a number representing the number of bins.')
            
    @property
    def bin_edges(self) -> np.ndarray:
        """
        Returns the edges of the bins.

        Returns
        -------
        np.ndarray
            The edges of the bins.
        """
        return self._bin_edges

    @property
    def bin_centers(self) -> np.ndarray:
        """
        Returns the centers of the bins.

        Returns
        -------
        np.ndarray
            The centers of the bins.
        """
        return bin_edge_to_bin_center(self.bin_edges)

    @property
    def bin_widths(self) -> np.ndarray:
        """
        Returns the widths of the bins.

        Returns
        -------
        np.ndarray
            The widths of the bins.
        """
        return np.diff(self.bin_edges)

    @property
    def nbins(self) -> int:
        """
        Returns the number of bins.

        Returns
        -------
        int
            The number of bins.
        """
        return len(self.bin_edges) - 1

    @property
    def bin_range(self) -> Tuple[float, float]:
        """
        Returns the bin range.

        Returns
        -------
        (float, float)
            The bin range.
        """
        return (self.bin_edges[0], self.bin_edges[-1])

    def is_uniform(self) -> bool:
        """
        Check if binning is uniform.

        Returns
        -------
        bool
            True if binning is uniform.
        """
        delta_widths = np.diff(self.bin_widths)
        return np.allclose(np.zeros(delta_widths.shape), delta_widths)