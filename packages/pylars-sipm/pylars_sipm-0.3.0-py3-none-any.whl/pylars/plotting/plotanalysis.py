"""Collection of usefull functions to plot results and analysis intermediate
steps.

The file is divided into LED OFF and LED ON sections. Most of the functions
provide the plt axis object to facility the integration of these plots in
different figures as required.
"""

from typing import Tuple, Union, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylars.utils.common import Gaussian, func_linear

from .plotprocessed import *

##### LED ON #####


def plot_area_LED(bv_dataset, voltage, LED_position=300,
                  log_y=True, full_x=False, ax=None,
                  color=None):
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    df = bv_dataset.data[voltage]

    cut_mask = ((df['position'] > (LED_position - 10)) &
                (df['position'] < (LED_position + 20)) &
                (df['length'] > 3))

    ax = plot_hist_area(df[cut_mask], ax=ax, color=color)

    if full_x:
        ax.set_xlim(0, 2**14 * 10 * 300)
    if log_y:
        ax.set_yscale('log')

    ax.set_title((f'LED ON\n module {bv_dataset.module} | '
                  f'channel {bv_dataset.channel[-1]}')
                 )

    med = np.median(df[cut_mask]['area'])
    std = np.std(df[cut_mask]['area'])
    med_err = std / np.sqrt(len(df[cut_mask]))

    return med, med_err, ax


def plot_LED_all_voltages(bv_dataset, cmap='winter', ax=None,):
    cm = plt.get_cmap(cmap)  # type: ignore
    N_lines = len(bv_dataset.voltages)

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    for i, _v in enumerate(bv_dataset.voltages):

        med, med_err, ax = plot_area_LED(bv_dataset, 50,
                                         color=cm(i / N_lines),
                                         ax=ax)
        ax.axvline(med, color=cm(i / N_lines))
        ax.set_title('')

    plt.show()


def plot_BV_fit(plot, temperature, voltages, gains,
                a, b, _breakdown_v, _breakdown_v_error, ax=None):

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6, 3), facecolor='white')

    ax.plot(gains, voltages,
            ls='', marker='x', c='k',
            label=(f'{temperature}K: ({_breakdown_v:.2f}'
                   f'$\\pm${_breakdown_v_error:.2f}) V')  # type: ignore
            )
    _offset_gains = min(gains) * 0.15
    _x = np.linspace(min(gains) - _offset_gains,
                     max(gains) + _offset_gains,
                     100)
    ax.plot(_x, func_linear(_x, a, b), c='r', alpha=0.9)
    ax.set_xlabel('Gain')
    ax.set_ylabel('Voltage [V]')
    ax.legend()
    ax.set_title(plot)
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0),
                        useMathText=True)

    if isinstance(plot, str):
        plt.tight_layout()
        plt.savefig(f'figures/{plot}_{temperature}_BV_fit.pdf')
        plt.close()
    else:
        return ax


def plot_BV_results(df_BV_results: pd.DataFrame,
                    all_channels: Union[list, tuple, np.ndarray],
                    r2_threshold: float = 0.,
                    ax=None):
    """Plot the distribution of BV voltages for different channels.

    Args:
        df_BV_results (pd.DataFrame): df with the BV values, errors, r2 value
            of linear fit for eahc temperature and channel.
        all_channels (Union[list, tuple, np.ndarray]): the channel names,
            in order, to put on the x axis ticks. Usually "(mod, ch)" or
            "#xxx" for the MPPC number.
        r2_threshold (float, optional): cuts BVs with fits with r2 bellow this
             value. Defaults to 0.
        ax (plt.axis, optional): the axis to draw into. Defaults to None.
    """
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))

    temps = df_BV_results.index.levels[0]  # type: ignore
    for t in temps:
        t_mask = ((df_BV_results['temp'] == t) &
                  (df_BV_results['r2'] > r2_threshold)
                  )
        _df = df_BV_results[t_mask]

        ax.errorbar(_df.index.codes[1],  # type: ignore
                    _df['BV'],
                    yerr=_df['BV_std'],
                    ls='', marker='.', capsize=4,
                    label=f'{t:.0f} K')

    ax.legend()
    ax.set_xticks(df_BV_results.index.levels[1],  # type: ignore
                  all_channels, rotation=30)

    return ax

##### LED OFF #####


def plot_DCR_curve(plot: Union[str, bool, None], area_hist_x: np.ndarray,
                   DCR_values: np.ndarray, _x: np.ndarray,
                   _y: np.ndarray, min_area_x: float, ax=None):
    """Make the DCR step plot.

    Args:
        plot (Optional[str]): string to save the fgiure with a name, None to
            return the axis
        area_hist_x (np.ndarray): x values on the step plot.
        DCR_values (np.ndarray): y values on the step plot.
        _x (np.ndarray): x values of the computed 1st derivative
        _y (np.ndarray): y values of the computed 1st derivative
        min_area_x (float): area of minimum of the derivative function
        ax (_type_, optional): Axis where to draw. Creates one if ax=None.
            Defaults to None.

    Returns:
        None or axis: the axis drawn at if `plot` not a str, None if `plot`
            is a string
    """

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 5), facecolor='white')
    ax.plot(area_hist_x, DCR_values,
            marker='x', ls='',
            c='k', label='Data points')
    ax.set_yscale('log')
    ax.set_xlabel('Area [integrated ADC counts]')
    ax.set_ylabel('# events')

    ax3 = ax.twinx()
    ax3.plot(_x, _y, c='r')
    ax3.tick_params(axis='y', labelcolor='r')
    ax3.axvline(min_area_x, c='r', ls='--', alpha=0.8,
                label='1$^{st}$ der. (smoothed)')
    ax3.set_ylabel('1$^{st}$ derivative')

    if 'fig' in locals():
        fig.legend()  # type: ignore

    if isinstance(plot, str):
        fig.savefig(f'figures/{plot}_stepplot.png')  # type: ignore
        plt.close()
    else:
        return ax


def plot_SPE_fit(df, length_cut_min, length_cut_max, plot, area_hist_x,
                 min_area_x, A, mu, sigma, ax=None):

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 5), facecolor='white')
    bin_size = area_hist_x[1] - area_hist_x[0]
    ax.hist(df[(df['length'] > length_cut_min) &
               (df['length'] < length_cut_max)]['area'],
            bins=np.linspace(0.5 * min_area_x, 1.5 * min_area_x, 300),
            color='gray', alpha=0.8)

    _x = np.linspace(area_hist_x[0], area_hist_x[-1], 200)
    ax.plot(_x, Gaussian(_x, A, mu, sigma), color='red')
    ax.set_xlabel('Area [integrated ADC counts]')
    ax.set_ylabel('# events')
    for i in range(1, 4):
        ax.axvline(mu * i, color='red', ls='--', alpha=0.7)
        # plt.yscale('log')

    if isinstance(plot, str):
        plt.savefig(f'figures/{plot}_1pe_fit.png')
        plt.close()
    else:
        return ax


def plot_found_area_peaks(area_x, area_y, area_filt, area_peaks_x,
                          plot=None, ax=None):

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 5), facecolor='white')

    ax.plot(area_x, area_y, color='k', alpha=0.7)  # , range = (100,1e4))

    ax.plot(area_x, area_filt, color='blue', ls='-', lw=1, alpha=1)

    ax.vlines(area_x[area_peaks_x], 0, 1e6, color='green', alpha=0.5)
    ax.set_xlabel('Area')
    ax.set_yscale('log')

    if isinstance(plot, str):
        plt.savefig(f'figures/{plot}_paeks_and_valeys.png')
        plt.close()
    elif plot is True:
        plt.show()


def plot_results_ds(results: pd.DataFrame,
                    errorbars: bool = True,
                    figaxs: Union[None, Tuple] = None) -> tuple:
    """Summary plot of the DCR results of run.

    Args:
        results (pd.DataFrame): results df
        errorbars (bool, optional): plot with errorbars. Defaults to True.
        figaxs (Union[None, Tuple], optional): where to draw the plots. Creates
            if None. Defaults to None.

    Returns:
        tuple: the figure and ax objects (fig,ax)
    """
    if figaxs is None:
        fig, axs = plt.subplots(4, sharex=True, sharey=False, figsize=(10, 8))
    else:
        fig, axs = figaxs
    fig.subplots_adjust(hspace=0)

    temps = np.unique(results['T'])
    for _temp in temps:
        _select = results['T'] == _temp
        if errorbars:
            axs[0].errorbar(results[_select]['Gain'],
                            results[_select]['V'],
                            xerr=results[_select]['Gain_error'],
                            ls='', capsize=4,
                            marker='.')  # , label = '180 K')
            axs[1].errorbar(results[_select]['Gain'],
                            results[_select]['SPE_res'],
                            xerr=results[_select]['Gain_error'],
                            yerr=results[_select]['SPE_res_error'],
                            ls='', capsize=4,
                            marker='.', label=f'{_temp:.0f} K')
            axs[2].errorbar(results[_select]['Gain'],
                            results[_select]['DCR'],
                            xerr=results[_select]['Gain_error'],
                            yerr=results[_select]['DCR_error'],
                            ls='', capsize=4,
                            marker='.')
            axs[3].errorbar(results[_select]['Gain'],
                            results[_select]['CTP'],
                            xerr=results[_select]['Gain_error'],
                            yerr=results[_select]['CTP_error'],
                            ls='', capsize=4,
                            marker='.')
        else:
            axs[0].plot(results[_select]['Gain'],
                        results[_select]['V'],
                        ls='',
                        marker='o', label=f'{_temp:.0f} K')
            axs[1].plot(results[_select]['Gain'], results[_select]['SPE_res'],
                        ls='',
                        marker='o')  # , label = '180 K')
            axs[2].plot(results[_select]['Gain'], results[_select]['DCR'],
                        ls='',
                        marker='o')
            axs[3].plot(results[_select]['Gain'], results[_select]['CTP'],
                        ls='',
                        marker='o')

    axs[0].set_ylabel('Bias Voltage [V]')
    axs[1].set_ylabel('SPE res [%]')
    axs[2].set_ylabel('DCR [Hz/mm$^2$]')
    axs[3].set_ylabel('CTP [%]')
    axs[3].set_ylim(0, 80)
    axs[-1].set_xlabel('Gain')
    axs[0].grid()
    axs[1].grid()
    axs[2].grid()
    axs[3].grid()

    fig.legend(bbox_to_anchor=[0.9, 0.84])

    return fig, axs


def plot_BV_DCRresults(df_BV_results: pd.DataFrame,
                       ch_names: Union[list, tuple, np.ndarray],
                       errorbars: bool = False,
                       figax=None) -> tuple:
    """Plot the distribution of BV voltages for different channels.

    Args:
        df_BV_results (pd.DataFrame): results of BV calculation from a DCR
            dataset with
            `pylars.analysis.breakdown.compute_BV_DCRds_results`
        ch_names(Union[list, tuple, np.ndarray]): names of the channels for
            the x axis
        errorbars (bool, optional): plot with errorbars. Defaults to True.
        figaxs (Union[None, Tuple], optional): where to draw the plots. Creates
            if None. Defaults to None.


    Returns:
        tuple: the figure and ax objects (fig,ax)
    """
    if figax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    else:
        fig, ax = figax

    temps = np.unique(df_BV_results['T'])

    for t in temps:
        _df = df_BV_results[df_BV_results['T'] == t]
        _df.reset_index(drop=True, inplace=True)

        if errorbars:
            ax.errorbar(_df.index, _df['BV'],
                        yerr=_df[f'BV_error'],
                        label=f'{t} K',
                        ls='', marker='.', capsize=4)

        else:
            ax.plot(_df.index, _df['BV'],
                    label=f'{t} K', ls='',
                    marker='o')
    ax.legend()
    ax.set_xticks(_df.index, ch_names, rotation=30)  # type: ignore
    fig.set_tight_layout(True)

    return fig, ax


def plot_parameter_for_V(results_df: pd.DataFrame, V: float,
                         parameter: str, ch_names: list,
                         errorbars: bool = False):
    """Plot the results from DCR analysis for a specific parameter
    (Gain, SPE_res, DCR, CTP) and applied voltage for all the recorded
    channels.

    Args:
        results_df (pd.DataFrame): DCR analysis results dataset.
        V (float): voltage.
        parameter (str): parameter to plot.
        ch_names (list): list with the names to assign to the channels.
        errorbars (bool, optional): include errorbars in plot. Defaults
            to False.

    Returns:
        (fig, ax): The figure and axis objects created.
    """

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    temps = np.unique(results_df['T'])
    for t in temps:
        _df = results_df[(results_df['V'] == V) & (results_df['T'] == t)]
        _df.reset_index(drop=True, inplace=True)

        if len(_df) == 0:
            print(f'Found no points for {V} V at {t} K.')
            continue

        if errorbars:
            ax.errorbar(_df.index, _df[parameter],
                        yerr=_df[f'{parameter}_error'],
                        label=f'{t} K',
                        ls='', marker='.', capsize=4)

        else:
            ax.plot(_df.index, _df[parameter],
                    label=f'{t} K', ls='',
                    marker='o')
    ax.legend(title=f'@{V} V')
    ax.set_ylabel(parameter)
    ax.set_xticks(_df.index, ch_names, rotation=30)  # type: ignore
    fig.set_tight_layout(True)

    return fig, ax
