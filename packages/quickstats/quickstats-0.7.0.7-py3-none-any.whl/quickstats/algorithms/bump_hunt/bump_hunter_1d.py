###############################################################################
### This is a reimplementation of pyBumpHunter package
### taken from https://github.com/scikit-hep/pyBumpHunter
### Original author: Louis Vaslin (main developer), Julien Donini
###############################################################################
from typing import Optional, Union, Tuple, List, Dict, Any, Callable
from itertools import repeat

import numpy as np
from scipy.special import gammainc as Gamma
from pydantic import Field

from quickstats import semistaticmethod
from quickstats.typing import ArrayLike
from quickstats.concepts import Binning
from quickstats.interface.pydantic import DefaultModel
from quickstats.maths.numerics import sliced_sum
from .settings import (
    BumpHuntMode,
    SignalStrengthScale,
    AutoScanStep
)

__all__ = ['BumpHunter1D']


class BumpHunter1D(DefaultModel):

    scan_range: Optional[Tuple[float, float]] = Field(default=None)
    mode: BumpHuntMode = Field(default=BumpHuntMode.Excess)
    width_min: int = Field(default=1)
    width_max: Optional[int] = Field(default=None)
    width_step: int = Field(default=1)
    scan_step: Union[int, AutoScanStep] = Field(default=1)
    npseudo: int = Field(default=100, gt=0)
    bins: Union[int, np.ndarray] = Field(default=60)
    parallel: int = Field(default=-1)
    sigma_limit: float = Field(default=5.0)
    mu_min: float = Field(default=0.5)
    mu_step: float = Field(default=0.25)
    mu_scale: SignalStrengthScale = Field(default=SignalStrengthScale.Linear)
    signal_exp: Optional[float] = Field(default=None)
    flip_sig: bool = Field(default=True)
    npseudo_inject: int = Field(default=100)
    seed: Optional[int] = Field(default=None)
    use_sideband: bool = Field(default=False)
    sideband_width: Optional[int] = Field(default=None)

    _pvalue_thres: float = 1e-300

    @staticmethod
    def _get_pval_algo(mode: Union[str, BumpHuntMode] = 'excess') -> Callable:
        """Get algorithm for evaluating local pvalues from slices of data and reference counts."""
        mode = BumpHuntMode.parse(mode)
        if mode == BumpHuntMode.Excess:
            def pval_algo(N_data: np.ndarray, N_ref: np.ndarray) -> np.ndarray:
                result = np.ones(N_data.size)
                mask = (N_data > N_ref) & (N_ref > 0)
                result[mask] = Gamma(N_data[mask], N_ref[mask])
                return result
            return pval_algo
        elif mode == BumpHuntMode.Deficit:
            def pval_algo(N_data: np.ndarray, N_ref: np.ndarray) -> np.ndarray:
                result = np.ones(N_data.size)
                mask = N_data < N_ref
                result[mask] = 1.0 - Gamma(N_data[mask] + 1, N_ref[mask])
                return result
            return pval_algo
        raise BumpHuntMode.on_parse_exception(mode)

    @staticmethod
    def _resolve_scan_steps(scan_step: Union[str, int] = 1, widths: np.ndarray) -> np.ndarray:
        """
        """
        # Auto-adjust scan step if specified.
        if isinstance(scan_step, int):
            steps = np.full(widths.shape, scan_step)
        else:
            scan_step = AutoScanStep.parse(scan_step)
            if scan_step == AutoScanStep.Full:
                steps = np.array(widths)
            elif scan_step == AutoScanStep.Half:
                steps = np.maximum(np.ones(widths.shape, dtype=int), widths // 2)
            else:
                raise AutoScanStep.on_parse_exception(scan_step)
        return steps

    @staticmethod
    def _get_index_bounds(ref: np.ndarray, sideband_width: Optional[int] = None) -> Tuple[int, int]:
        nonzero_indices = np.where(ref > 0)[0]
        idx_inf = np.min(nonzero_indices)
        idx_sup = np.max(nonzero_indices) + 1
        if sideband_width is not None:
            idx_inf += sideband_width
            idx_sup -= sideband_width
        return idx_inf, idx_sup

    @staticmethod
    def _get_sideband_norm(data: np.ndarray, ref: np.ndarray) -> Tuple[float, float]:
        idx_inf, idx_sup = BumpHunter1D._get_index_bounds(ref)
        data_total = data[idx_inf:idx_sup].sum()
        ref_total = ref[idx_inf:idx_sup].sum()
        return data_total, ref_total

    @semistaticmethod
    def _scan_hist(
        self,
        data: np.ndarray,
        ref: np.ndarray,
        widths: np.ndarray,
        mode: Union[str, BumpHuntMode] = 'excess',
        scan_step: Union[str, int] = 1,
        use_sideband: bool = False,
        sideband_width: Optional[int] = None,
        detailed: bool = True
    ) -> Dict[str, Any]:
        """Scan a distribution and compute the p-value associated to every scan window.

        The algorithm follows the BumpHunter algorithm. Compute also the significance for the data histogram.
        """
        data = np.asarray(data)
        ref = np.asarray(ref)
        widths = np.asarray(widths, dtype=int)

        if np.ndim(data) != 1:
            raise ValueError(f'Target histogram must be one-dimensional, got {np.ndim(data)} instead.')
        if np.ndim(ref) != 1:
            raise ValueError(f'Reference histogram must be one-dimensional, got {np.ndim(ref)} instead.')
        if data.shape != ref.shape:
            raise ValueError(f'Target and reference histograms must have the same shape.')
        if np.ndim(widths) != 1:
            raise ValueError(f'Widths array must be one-dimensional, got {np.ndim(widths)} instead.')
        if not use_sideband:
            sideband_width = None

        # remove the first/last hist bins if empty ... just to be consistent with c++
        data_inf, data_sup = self._get_index_bounds(ref, sideband_width=sideband_width)
        if use_sideband:
            data_total, ref_total = self._get_sideband_norm(data, ref)
        else:
            data_total, ref_total = None, None

        steps = self._resolve_scan_steps(scan_step, widths)
        pval_algo = self._get_pval_algo(mode)

        pval_arr = np.empty(widths.shape, dtype=object)
        delta_arr = np.zeros(widths.shape)
        scale_arr = np.ones(widths.shape)

        for i, (width, step) in enumerate(zip(widths, steps)):
            # define position range
            pos = np.arange(data_inf, data_sup - width + 1, step)

            # check that there is at least one interval to check for a given width
            # if not, we must set dummy values in order to avoid crashes
            if not pos.size:
                pval_arr[i] = np.array([1.0])
                continue

            slices = np.stack([pos, pos + width], axis=1)
            N_data = sliced_sum(data, slices)
            N_ref = sliced_sum(ref, slices)

            # compute and apply side-band normalization scale factor (if needed)
            if use_sideband:
                scale = (data_total - N_data) / (ref_total - N_ref)
                N_ref *= scale
                scale_arr[i] = scale

            pval = pval_algo(N_data, N_ref)

            if use_sideband:
                # prevent issue with very low p-value, sometimes induced by normalization in the tail
                pval = np.minimum(pval, self._pvalue_thres)

            pval_arr[i] = pval
            delta_arr[i] = N_data - N_ref

        # get the minimum p-value and associated window among all width
        min_pvals = np.array(list(map(np.min, pval_arr)))
        min_locs = np.array(list(map(np.argmin, pval_arr)))
        idx = min_pvals.argmin()

        result = {
            'pval_arr': pval_arr,
            'min_pval': min_pvals[idx],
            'min_width': widths[idx],
            'min_loc': min_locs[idx],
            'signal_eval': delta_arr[idx][min_locs[idx]],
            'norm_scale': scale_arr[idx] if use_sideband else None
        }
        if not detailed:
            result.pop('pval_arr')
        return result

    @semistaticmethod
    def _default_result_multi(
        self,
        data_list: List[np.ndarray],
        ref_list: List[np.ndarray],
        widths: np.ndarray,
        sideband_width: Optional[int] = None
    ) -> Dict[str, Any]:
        nchannel = len(data_list)
        data_inf_list = []
        data_sup_list = []
        for i in range(nchannel):
            data_inf, data_sup = self._get_index_bounds(ref_list[i], sideband_width=sideband_width)
            data_inf_list.append(data_inf)
            data_sup_list.append(data_sup)
        pval_arr = np.ones((nchannel, widths.size, 1.0))
        result = {
            'pval_arr': pval_arr,
            'min_pval': np.ones(nchannel),
            'min_loc': np.array(data_inf_list),
            'min_width': np.array(data_sup_list),
            'signal_eval': np.zeros(nchannel),
            'norm_scale': None
        }
        return result

    @staticmethod
    def _combine_result(
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        combined_result = {
            'pval_arr': [],
            'min_pval': [],
            'min_loc': [],
            'min_width': [],
            'norm_scale': []
        }
        for result in results:
            if 'pval_arr' in result:
                combined_result['pval_arr'].append(result['pval_arr'])
            combined_result['min_pval'].append(result['min_pval'])
            combined_result['min_loc'].append(result['min_loc'])
            combined_result['min_width'].append(result['min_width'])
            combined_result['norm_scale'].append(result['norm_scale'])
        return combined_result

    @staticmethod
    def _combine_channel_result(
        data_list: List[np.ndarray],
        ref_list: List[np.ndarray],
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        combined_result = BumpHunter1D._combine_result(results)
        combined_result['signal_eval'] = []
        for data, ref, result in zip(data_list, ref_list, results):
            start, end = result['min_loc'], result['min_loc'] + result['min_width']
            signal_eval = data[start:end].sum() - ref[start:end].sum()
            combined_result['signal_eval'].append(signal_eval)
        return combined_result

    @semistaticmethod
    def _scan_hist_multi(
        self,
        data_list: Union[np.ndarray, List[np.ndarray]],
        ref_list: Union[np.ndarray, List[np.ndarray]],
        widths: np.ndarray,
        binning_list: List[Binning],
        mode: Union[str, BumpHuntMode] = 'excess',
        scan_step: Union[str, int] = 1,
        use_sideband: bool = False,
        sideband_width: Optional[int] = None,
        detailed: bool = True
    ) -> Dict[str, Any]:
        """
        Scan a distribution in multiple channels and compute the p-value associated to every scan window.

        The algorithm follows the BumpHunter algorithm extended to multiple channels.
        """
        widths = np.asarray(widths)

        if not len(data_list):
            raise ValueError(f'Data list is empty.')
        if not len(ref_list):
            raise ValueError(f'Reference list is empty.')

        if not isinstance(data_list, (list, np.ndarray)):
            raise ValueError(f'Multi-channel data histograms must be a list of 1D arrays or 2D arrays of shape '
                             f'(nchannel, nbins), got {type(data_list).__name__} instead.')
        if not isinstance(ref_list, (list, np.ndarray)):
            raise ValueError(f'Multi-channel reference histograms must be a list of 1D arrays or 2D arrays of shape '
                             f'(nchannel, nbins), got {type(ref_list).__name__} instead.')
        if len(data_list) != len(ref_list):
            raise ValueError(f'Number of channels for data (= {len(data_list)}) and reference (= {len(ref_list)}) histograms must be equal.')
        if len(data_list) != len(binning_list):
            raise ValueError(f'Number of channel binnings (= {len(binning_list)}) must equal the number of channels (= {len(data_list)})')

        data_list = [np.asarray(data) for data in data_list]
        ref_list = [np.asarray(ref) for ref in ref_list]
        nchannel = len(data_list)

        for i, (data, ref) in enumerate(zip(data_list, ref_list)):
            if np.ndim(data) != 1:
                raise ValueError(f'(Channel {i + 1}) Target histogram must be one-dimensional, got {np.ndim(data)} instead.')
            if np.ndim(ref) != 1:
                raise ValueError(f'(Channel {i + 1}) Reference histogram must be one-dimensional, got {np.ndim(ref)} instead.')
            if data.shape != ref.shape:
                raise ValueError(f'Inconsistent shapes between data (= {data.shape}) and reference (= {ref.shape}) histograms in channel {i + 1}.')

        if nchannel == 1:
            return self._scan_hist(data_list[0], ref_list[0],
                                   widths=widths,
                                   mode=mode,
                                   scan_step=scan_step,
                                   use_sideband=use_sideband,
                                   sideband_width=sideband_width,
                                   detailed=detailed)

        if not use_sideband:
            sideband_width = None

        def get_loc_right(res: Dict[str, Any]) -> float:
            return res['min_loc'] + res['min_width']

        results = []
        for channel_idx in range(len(data_list)):
            data = data_list[channel_idx]
            ref = ref_list[channel_idx]
            result = self._scan_hist(
                data, ref, widths,
                mode=mode,
                scan_step=scan_step,
                use_sideband=use_sideband,
                sideband_width=sideband_width
            )
            results.append(result)

            if channel_idx == 0:
                continue

            result_prev = results[channel_idx - 1]

            # get the right edge of the bump
            loc_right_curr = get_loc_right(result)
            loc_right_prev = get_loc_right(result_prev)

            binning_curr = binning_list[channel_idx]
            binning_prev = binning_list[channel_idx - 1]
            bin_edges_curr = binning_curr.bin_edges
            bin_edges_prev = binning_prev.bin_edges

            # no overlap, we can break the loop
            if (bin_edges_curr[loc_right_curr] <= bin_edges_prev[result_prev['min_loc']] or
                bin_edges_curr[result['min_loc']] >= bin_edges_prev[loc_right_prev]):
                combined_result = self._default_result_multi(data_list, ref_list, widths, sideband_width)
                break
            # there is an overlap, we can update the global results
            else:
                # check left bound of overlap interval
                if bin_edges_curr[result['min_loc']] < bin_edges_prev[result_prev['min_loc']]:
                    while bin_edges_curr[result['min_loc']] < bin_edges_prev[result_prev['min_loc']]:
                        result['min_loc'] += 1
                    result['min_loc'] -= 1
                # check right bound of overlap interval
                if bin_edges_curr[loc_right_curr] < bin_edges_prev[loc_right_prev]:
                    while bin_edges_curr[loc_right_curr] < bin_edges_prev[loc_right_prev]:
                        loc_right_curr -= 1
                    loc_right_curr += 1
                result['min_width'] = loc_right_curr - result['min_loc']
        else:
            combined_result = self._combine_channel_result(data_list, ref_list, results)

        if not detailed:
            combined_result.pop('pval_arr')
        return combined_result

    @staticmethod
    def _make_binned(data: np.ndarray, ref: np.ndarray, bins: Union[int, np.ndarray],
                     bin_range: Optional[ArrayLike] = None,
                     weights: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray, Binning]:
        ref_hist, edges = np.histogram(ref,
                                       bins=bins,
                                       range=bin_range,
                                       weights=weights)
        binning = Binning(bins=edges)
        data_hist, edges = np.histogram(data,
                                        bins=binning.bin_edges)
        return data_hist, ref_hist, binning

    def bump_scan(
        self,
        data: Union[np.ndarray, List[np.ndarray]],
        ref: Union[np.ndarray, List[np.ndarray]],
        weights: Optional[Union[np.ndarray, List[np.ndarray]]] = None,
        binned: bool = False,
        do_pseudo: bool = True
    ) -> Dict[str, Any]:
        """
        Perform the full BumpHunter algorithm presented in https://arxiv.org/pdf/1101.0390.pdf without sidebands.
        This includes the generation of pseudo-data, the calculation of the BumpHunter p-value associated to data and to all pseudo experiment 
        as well as the calculation of the test statistic t.

        Arguments :
            data :
                The data distribution.
                If there is only one channel, it should be a numpy array containing the data distribution.
                Otherwise, it should be a list of numpy arrays (one per channel).
                The distribution(s) will be transformed into a binned histogram and the algorithm will look for the most significant excess.

            ref :
                The reference background distribution.
                If there is only one channel, it should be a numpy array containing the reference background distribution.
                Otherwise, it should be a list of numpy arrays (one per channel).
                The distribution(s) will be transformed into a binned histogram and the algorithm will compare it to data while looking for a bump.

            weights :
                An optional array of weights for the reference distribution.

            binned :
                Boolean that specifies if the given data and background are already in histogram form.
                If true, the data and background are considered as already 'histogramed'.
                Default to False.

            do_pseudo :
                Boolean specifying if pseudo data should be generated.
                If False, then the BumpHunter statistics distribution kept in memory is used to compute the global p-value and significance.
                If there is nothing in memory, the global p-value and significance will not be computed.
                Default to True.
        """
        
        # Set the seed if required (or reset it if None)
        np.random.seed(self.seed)

        if not len(data):
            raise ValueError(f'Data array is empty.')
        if not len(ref):
            raise ValueError(f'Reference array is empty.')
        if np.ndim(data[0]) == 0:
            nchannel = 1
            data = [np.asarray(data)]
            ref = [np.asarray(ref)]
        elif np.ndim(data[0]) == 1:
            nchannel = len(data)
            data = [np.asarray(data_i) for data_i in data]
            ref = [np.asarray(ref_i) for ref_i in ref]
            if len(data) != len(ref):
                raise ValueError(f'Inconsistent number of channels between data (= {len(data)}) '
                                 f'and reference (= {len(ref)}).')
            if (weights is not None) and (len(weights) != nchannel):
                raise ValueError(f'Size of weights (= {len(weights)}) does not match the number of channels.')
        else:
            raise ValueError(f'Data distribution must be one-dimensional, got ndim = {np.ndim(data[0])} instead.')
            
        if binned:
            for i in range(nchannel):
                if data[i].shape != ref[i].shape:
                    raise ValueError(f'Inconsistent shapes between data (= {data[i].shape}) and reference '
                                     f'(= {ref[i].shape}) histograms in channel {i + 1}.')
                    
        default_bins = [self.bins] * nchannel
        if weights is None:
            weights = [None] * nchannel
        
        self.stdout.info('Generating histograms.')
        data_list, ref_list, binning_list, pseudo_list = [], [], [], []
        for i in range(nchannel):
            if not binned:
                data_hist, ref_hist, binning = self._make_binned(data[i], ref[i],
                                                                 bins=default_bins[i],
                                                                 bin_range=self.scan_range,
                                                                 weights=weights[i])

            else:
                data_hist = data[i]
                if weights[i] is not None:
                    ref_hist = ref[i] * weights[i]
                else:
                    ref_hist = ref[i]
                binning = default_bins[i]
            data_list.append(data_hist)
            ref_list.append(ref_hist)
            binning_list.append(binning)
            # generate pseudo-data histograms
            if do_pseudo:
                lam = np.tile(ref_hist, (self.npseudo, 1)).transpose()
                size = (ref_hist.size, self.npseudo)
                pseudo_hist = np.random.poisson(lam=lam, size=size)
                pseudo_list.append(pseudo_hist)
            
        if pseudo_list:
            pseudo_list = np.array(pseudo_list)
            # shape = (npseudo, nchannel, nbins)
            pseudo_list = np.transpose(pseudo_list, (2, 0, 1))
            # shape = (npseudo + 1, nchannel, nbins)
            all_data_list = np.concatenate([np.array([data_list]), pseudo_list])
            detailed = [True] + [False] * self.npseudo
        else:
            # shape = (1, nchannel, nbins)
            all_data_list = np.expand_dims(data_list, 0)
            detailed = [True]

        if nchannel > 1:
            bin_edges = binning_list[0].bin_edges
            for i in range(1, nchannel):
                if not np.allclose(bin_edges, binning_list[i].bin_edges):
                    raise RuntimeError('Inconsistent binnings across channels.')

        if self.width_max is None:
            width_max = data_list[0].size // 2
        else:
            width_max = self.width_max

        widths = np.arange(self.width_min, width_max + 1, self.width_step)
        self.stdout.info(f'Number of widths to be tested: {widths.size}')

        results = execute_multi_tasks(self._scan_hist_multi,
                                      all_data_list,
                                      repeat(ref_list),
                                      repeat(widths),
                                      repeat(binning_list),
                                      repeat(self.mode),
                                      repeat(self.scan_step),
                                      repeat(self.use_sideband),
                                      repeat(self.sideband_width),
                                      detailed,
                                      parallel=self.parallel)
        results = self._combine_result(results)

        if nchannel == 1:
            results['nll'] = - np.log(results['min_pval'])
        else:
            results['nll'] = - np.log(np.prod(results['min_pval'], axis=1))

        # Compute the global p-value from the nll distribution
        nll_array = combined_results['nll']
        nll_data = nll_array[0]
        nll_pseudo = nll_array[1:]
        if nll_array.size > 1:
            S = nll_pseudo[nll_pseudo >= nll_data].size
            global_pval = S / self.npseudo
            self.stdout.info(f'Global p-value : {global_pval:1.4f} ({S} / {self.npseudo})')

            # check global p-value
            if global_pval == 1:
                significance = 0
                self.stdout.info(f'Significance = {significance}')
            elif global_pval == 0:
                # in this case, we can't compute directly the significance, so we set a limit
                significance = norm.ppf(1 - (1 / self.npseudo))
                self.stdout.info(f'Significance > {significance:1.5f} (lower limit)')
            else:
                significance = norm.ppf(1 - global_pval)
                self.stdout.info(f'Significance = {significance:1.5f}')
        else:
            self.stdout.info('No pseudo data found : cannot compute global p-value')
    
        pval_arr = combined_results.pop('pval_arr')[0]
        summary = {
            'data_pval_arr': pval_arr,
            'results': results,
            'global_pval': global_pval,
            'significance': significance
        }
        self.summary = summary
        return summary