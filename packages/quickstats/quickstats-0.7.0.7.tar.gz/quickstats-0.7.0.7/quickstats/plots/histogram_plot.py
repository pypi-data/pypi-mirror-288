from typing import Optional, Union, Dict, List, Tuple, Callable, Sequence


from quickstats.utils.common_utils import combine_dict


import numpy as np
import matplotlib

from quickstats import AbstractObject, semistaticmethod
from quickstats.core.typing import ArrayLike
from quickstats.plots.template import (single_frame, ratio_frame,
                                       parse_styles, format_axis_ticks,
                                       parse_analysis_label_options, centralize_axis,
                                       create_transform, draw_multiline_text,
                                       CUSTOM_HANDLER_MAP)
from quickstats.utils.common_utils import combine_dict, insert_periodic_substr
from quickstats.maths.statistics import (
    bin_center_to_bin_edge, get_hist_comparison_data,
    select_binned_data, get_histogram_mask, upcast_error,
    HistoMaskType, HistComparisonMode
)
from quickstats.maths.numerics import get_subsequences

from .abstract_plot import AbstractPlot

ErrorDataType = Union[Tuple[np.ndarray, np.ndarray], np.ndarray]

class HistogramPlot(AbstractObject):

    @staticmethod
    def _mask_binned_data(data:Dict[str, ArrayLike], condition:HistoMaskType):
        # making copies
        result = {
            'x': np.array(data['x']),
            'y': np.array(data['y']),
            'xerr': np.array(data['xerr']) if data['xerr'] is not None else None,
            'yerr': np.array(data['yerr']) if data['xerr'] is not None else None
        }
        mask = get_histogram_mask(data['x'], condition=condition, y=data['y'])
        
        def apply_mask(array:Optional[ArrayLike], mask:np.ndarray):
            if array is None:
                continue
            if np.ndim(array) == 2:
                array[0][mask] = 0.
                array[1][mask] = 0.
            array[mask] = 0.
            
        for key in ['y', 'xerr' , 'yerr']:
            apply_mask(result[key], mask)
            
        return result

    @staticmethod
    def _process_binned_data(data:Dict[str, ArrayLike],
                             hide:Optional[Union[HistoMaskType, List[HistoMaskType]]=None):
        x, y = np.asarray(data['x']), np.asarray(data['y'])
        if x.ndim not in {1, 2}:
            raise ValueError(f'Binned data must be 1D or 2D, but got {x.ndim}D.')
        if x.shape != y.shape:
            raise ValueError(f'x and y must have the same shape, but got ({x.shape) and ({y.shape}).')
        if x.ndim == 1:
            
        for key in ['xerr', 'yerr']:
            if x.ndim == 2:
                size = x.shape[0]
                err = data.get(key)
                if err is not None:
                    if len(err) != size:
                        raise ValueError(f'Size of x (={size}) does not match size of {key}(={len(err)}).')
                    result[key] = [upcast_error(err_i) for err_i in err]
                else:
                    result[key] = [None] * size
            else:
                result[key] = upcast_error(data.get(key))
                
                    
        if x.
        if x.ndim == 2:
            
        ndim = x.ndim
        x, y = data['x'], data['y']
        if isinstance(x, list):
            
        
                'xerr': upcast_error(data.get('xerr')),
                'yerr': upcast_error(data.get('yerr'))
        if ndim not in [1, 2]:
            raise ValueError(f'Binned data must be 1D or 2D, but got {ndim}D.')
        # do not cast x and y to array since matplotlib histogram treats list of arrays
        # and 2D array differently when doing stacked plot

        nbins = result['x'].shape[-1]
        # stacked data
        if result['x'].ndim == 2:
            ndata = result['x'].shape[0]
            for key in ['xerr', 'yerr']:
                errs = data.get(key, None)
                if errs is None:
                    result[key] = [None] * ndata
                    continue
                if len(errs) != ndata:
                    raise ValueError(f'"{key}" (size: {len(errs)}) does not have size '
                                     'matching that of "x" (size: {ndata})')
                result[key] = [upcast_error(size, err) for err in errs]
        else:
            result['xerr'] = upcast_error(size, data.get('xerr', None))
            result['yerr'] = upcast_error(size, data.get('yerr', None))
        return result

    def _draw_hist(self, ax, data:Dict[str, ArrayLike],
                   bin_edges:Optional[np.ndarray]=None,
                   styles:Optional[Dict]=None):
        x, y = data['x'], data['y']
        styles = self.get_combined_styles('hist', styles)
        stacked = np.ndim(x) == 2
        if stacked and (not styles.get("stacked")):
            raise ValueError('Binned data is 2-dimensional but the stacked option is not set.')
        # deduce bin edges from bin centers, assuming uniform binning
        if bin_edges is None:
            # stacked data
            if stacked:
                bin_edges_list = [bin_center_to_bin_edge(x_i) for x_i in x]
                if not all(np.array_equal(bin_edges, bin_edges_list[0]) \
                           for bin_edges in bin_edge_list):
                    raise ValueError('Stacked histograms must have the same binning.')
                bin_edges = bin_edges_list[0]
            else:
                bin_edges = bin_center_to_bin_edge(x)
        hist_y, _, handles = ax.hist(x, weights=y, bins=bins, **styles)
        def check_consistency(y1:np.ndarray, y2:np.ndarray) -> None:
            if not np.allclose(y1, y2):
                raise RuntimeError('Histogram bin values do not match the supplied '
                                   'weights. Please check your inputs.')
        # make sure bin value matches the y value
        if stacked:
            y0 = 0.
            for hist_y_i, y_i in zip(hist_y, y):
                check_consistency(hist_y_i - y0, y_i)
                y0 += hist_y_i
        else:
            check_consistency(hist_y, y)
        return handles
        
    def _draw_errorbar(self, ax, data:Dict[str, ArrayLike],
                       styles:Optional[Dict]=None):
        styles = self.get_combined_styles('errorbar', styles)
        handle = ax.errorbar(**data, **styles)
        return handle

    def _draw_filled(self, ax, data:Dict[str, ArrayLike],
                     bin_edges:Optional[np.ndarray]=None,
                     styles:Optional[Dict]=None):
        x, y = data['x'], data['y']
        xerr, yerr = data.get('xerr', None), data.get('yerr', None)
        if bin_edges is None:
            bin_edges = bin_center_to_bin_edge(x)
        # handle cases where data is not continuous
        indices = np.arange(np.shape(x)[0])
        mask = y > 0.
        sections_indices = get_subsequences(indices, mask, min_length=2)
        handles = []
        styles = self.get_combined_styles('fill_between', styles)
        for indices in sections_indices:
            mask = np.full(x.shape, False)
            mask[section_indices] = True
            x_i, y_i, xerr_i, yerr_i = select_binned_data(mask, x, y, xerr, yerr)
            # extend to edge
            x_i[0] = bin_edges[section_indices[0]]
            x_i[-1] = bin_edges[section_indices[-1] + 1]
            if (np.ndim(yerr_i) == 2) and (np.shape(yerr_i)[0] == 2):
                yerrlo = y_i - yerr_i[0]
                yerrhi = y_i + yerr_i[1]
            else:
                yerrlo = y_i - yerr_i
                yerrhi = y_i + yerr_i
            handle = ax.fill_between(x_i, yerrlo, yerrhi, **styles)
            handles.append(handle)
        return handles[0]

    def _draw_shades(self, data:Dict[str, ArrayLike],
                     bin_edges:Optional[np.ndarray]=None,
                     styles:Optional[Dict]=None):
        x, y = data['x'], data['y']
        yerr = data.get('yerr', None)
        if yerr is None:
            yerr = 0.
        if bin_edges is None:
            bin_edges = bin_center_to_bin_edge(x)
        bin_widths = np.diff(bin_edges)
        if (np.ndim(yerr) == 2) and (np.shape(yerr)[0] == 2):
            height = yerr[0] + yerr[1]
            bottom = y - yerr[0]
        else:
            height = 2 * yerr
            bottom = y - yerr
        styles = self.get_combined_styles('bar', styles)
        handle = ax.bar(x=x, height=height, bottom=bottom,
                        width=bin_widths, **styles)
        return handle



    @staticmethod
    def _process_binned_data(data:Dict[str, ArrayLike],
                             mask_condition:Optional[Union[HistoMaskType, List[HistoMaskType]]=None):
        result = {
            
        }
        x, y = data['x'], data['y']
        ndim = np.ndim(x)
        if ndim not in [1, 2]:
            raise ValueError(f'Binned data must be 1D or 2D, but got {ndim}D.')
        # do not cast x and y to array since matplotlib histogram treats list of arrays
        # and 2D array differently when doing stacked plot
        shape_x, shape_y = np.shape(x), np.shape(y)
        if shape_x != shape_y:
            raise ValueError(f'x and y must have same shape, but got ({shape_x) and ({shape_y})')
        
        multi_data = np.ndim(

    
        
    def draw_binned_data(self, ax, data:Dict[str, ArrayLike],
                         bin_edges:Optional[np.ndarray]=None,
                         hide:Optional[Union[HistoMaskType, List[HistoMaskType]]=None,
                         draw_data:bool=True,
                         draw_error:bool=True,
                         plot_format:Union[PlotFormat, str]='errorbar',
                         error_format:Union[ErrorDisplayFormat, str]='errorbar',
                         styles:Optional[Dict]=None,
                         error_styles:Optional[Dict]=None):
        if (not draw_data) and (not draw_error):
            raise ValueError('Nothing to draw.')
        if hide is not None:
            data = self._mask_binned_data(data, hide)
        plot_format  = PlotFormat.parse(plot_format)
        error_format = ErrorDisplayFormat.parse(error_format)
        handle, error_handle = None, None
        
        if draw_data:
            if plot_format == PlotFormat.HIST:
                handle = self._draw_hist_from_binned_data(ax, data,
                                                          bin_edges=bin_edges,
                                                          styles=styles)
            elif plot_format == PlotFormat.ERRORBAR:
                if (not draw_error) or (error_format != ErrorDisplayFormat.ERRORBAR):
                    handle = self._draw_errorbar(ax, data, styles=styles)
                else:
                    handle = self._draw_errorbar(ax, data, styles=styles)
            else:
                raise RuntimeError(f'unsupported plot format: {plot_format.name}')
                
        if draw_error:
            if error_format == ErrorDisplayFormat.FILL:
                error_handle = self._draw_fill_from_binned_data(ax, data, 
                                                                styles={**error_styles,
                                                                        "zorder": -1})
            elif error_format == ErrorDisplayFormat.SHADE:
                error_handle = self._draw_shade_from_binned_data(ax, data,
                                                                 bin_edges=bin_edges,
                                                                 styles={**error_styles,
                                                                        "zorder": -1})
            elif ((error_format == ErrorDisplayFormat.ERRORBAR) and
                 ((not draw_data) or (plot_format !=PlotFormat.ERRORBAR))):
                error_handle = self._draw_errorbar(ax, data,
                                                   styles={**error_styles,
                                                           "marker": 'none'})
        if isinstance(handle, list):
            handle = handle[0]
        handles = tuple([h for h in [handle, error_handle] if h is not None])
        return handles

    def draw_stacked_binned_data(self, ax, data,
                                 draw_data:bool=True,
                                 draw_error:bool=True,
                                 bin_edges:Optional[np.ndarray]=None,
                                 plot_format:Union[PlotFormat, str]='errorbar',
                                 error_format_list:Union[ErrorDisplayFormat, str]='errorbar',
                                 styles:Optional[Dict]=None,
                                 hide_list:Optional[List[Union[HistoMaskType, List[HistoMaskType]]]=None,
                                 error_styles_list:Optional[Dict]=None):
        if (not draw_data) and (not draw_error):
            raise ValueError('can not draw nothing')
        n_component = len(data['x'])
        if styles is None:
            styles = {}
        if error_styles_list is None:
            error_styles_list = [{}] * n_component
        plot_format  = PlotFormat.parse(plot_format)
        error_format_list = [ErrorDisplayFormat.parse(fmt) for fmt in error_format_list]
        handles, error_handles = None, None
        
        x_list, y_list = data['x'], data['y']
        xerr_list, yerr_list = data.get('xerr', None), data.get('yerr', None)
        if draw_data:
            if plot_format == PlotFormat.HIST:
                plot_func = self._draw_stacked_hist_from_binned_data
                hist_y, handles = plot_func(ax, x_list, y_list,
                                            bin_edges=bin_edges,
                                            hide_list=hide_list,
                                            styles=styles)
            else:
                raise RuntimeError(f'unsupported format for stacked plot: {plot_format.name}')
        if draw_error:
            error_handles = []
            def get_component(obj, index):
                if obj is not None:
                    return obj[index]
                return None
            for i in range(n_component):
                error_format = error_format_list[i]
                x, y = x_list[i], hist_y[i]
                xerr = get_component(xerr_list, i)
                yerr = get_component(yerr_list, i)
                hide = get_component(hide_list, i)
                error_styles = get_component(error_styles_list, i)
                if error_format == ErrorDisplayFormat.FILL:
                    error_handle = self._draw_fill_from_binned_data(ax, x, y, yerr=yerr,
                                                                    hide=hide,
                                                                    styles={**error_styles,
                                                                            "zorder": -1})
                elif error_format == ErrorDisplayFormat.SHADE:
                    error_handle = self._draw_shade_from_binned_data(ax, x, y, yerr=yerr,
                                                                     bin_edges=bin_edges,
                                                                     hide=hide,
                                                                     styles={**error_styles,
                                                                            "zorder": -1})
                elif error_format == ErrorDisplayFormat.ERRORBAR:
                    error_handle = self._draw_errorbar(ax, x, y,
                                                       xerr=xerr, yerr=yerr,
                                                       hide=hide,
                                                       styles={**error_styles,
                                                               "marker": 'none'})
                error_handles.append(error_handle)
        if error_handles is None:
            return handles
        if handles is None:
            return error_handles
        handles = [(handle, error_handle) for handle, error_handle in zip(handles, error_handles)]
        return handles