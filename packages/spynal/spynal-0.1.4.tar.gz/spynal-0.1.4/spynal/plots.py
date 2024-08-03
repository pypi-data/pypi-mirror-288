#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions for generating common data plots and plotting-related utilities

Overview
--------
High-level interfaces to create plot types commonly used in neuroscience, including heat maps,
line/curve plots with tranparent fills indicating errors, and offset lineseries plots (eg for
plotting series of ephys traces or evoked potentials).

Also contains some utility functions useful in generating plots.

Built using `matplotlib.pyplot` functions.


Function list
-------------
Plot-generating functions
^^^^^^^^^^^^^^^^^^^^^^^^^
- plot_line_with_error_fill :   Plot 1d data as line(s) w/ transparent fill(s) to indicate errors
- plot_heatmap :                Plot 2d data as a heatmap (pseudocolor) plot
- plot_lineseries :             Plot 2d data as series of offset lines

Plotting utilities
^^^^^^^^^^^^^^^^^^
- full_figure :                 Create full-screen figure
- savefig :                     Save figure to file in ~WYSIWYG manner
- make_colormap :               Create custom colormap and register name for further use
- colorbar :                    Create colorbar without messing up parent axis size/shape
- plot_markers :                Plot set of markers (eg to mark trial event times) on given axis(s)

Function reference
------------------
"""
# Created on Tue Nov 23 14:22:47 2021
#
# @author: sbrincat
import os
from warnings import warn
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import get_backend
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.image import AxesImage
from matplotlib.patches import Polygon
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from spynal.utils import isnumeric, isarraylike
from spynal.helpers import _isint, _merge_dicts

# Lambda returns list of all settable attributes of given plotting object
# Find all methods starting with 'set_***', strip out the 'set_', and place in a list
_settable_attributes = lambda obj: ['_'.join(attr.split('_')[1:]) for attr in dir(obj) \
                                    if attr.startswith('set_')]

# Create list of all settable attributes/parameters of plotting objects/functions used in module
AXES_PARAMS = _settable_attributes(Axes)
PLOT_PARAMS = ['scalex', 'scaley'] + _settable_attributes(Line2D)
FILL_PARAMS = _settable_attributes(Polygon)
# For some reason, imshow has several settable params that aren't AxesImage attributes...
# this seems to be a way to get them (though not for other functions...?)
IMSHOW_PARAMS = ['aspect','origin'] + _settable_attributes(AxesImage)


# =============================================================================
# Functions to generate specific plot types
# =============================================================================
def plot_line_with_error_fill(x, data, err=None, ax=None, color=None, events=None, **kwargs):
    """
    Plot 1d data as line plot(s) +/- error(s) as semi-transparent fill(s) in given axis

    Can plot multiple lines/errors with same x-axis values in same axis by inputting
    multiple data/error series

    Uses :func:`plt.plot` and :func:`plt.fill`

    Parameters
    ----------
    x : array-like, shape=(n,)
        x-axis sampling vector for both `data` and `err`.

    data : array-like, shape=(n,) or (n_lines,n)
        Values to plot on y-axis as line(s) (typically means or medians).
        To plot multiples lines with the same x-axis values, input a 2D array where
        each row will be plotted as a separate line.

    err : array-like, shape=(n,) or (n_lines,n) or (2*n_lines,n), default: (no errorbars)
        Error values (SEMs/confints/etc.) to plot as semi-transparent fill around line(s).

        If vector-valued or (n_lines,n) array, errors are treated as 1-sided (like SEMs),
        and `data[j,:]` +/- `err[j,:]` is plotted for each line j.

        If given as (2*n_lines,n) array, it's treated as 2-sided [upper; lower] error ranges
        (like confidence intervals), with the odd rows = upper and even rows = lower errors
        corresponding to each line.

        If err=None [default], only the data line(s) are plotted without error fills
        (to simplify calling code with optional errors).

    color : Color spec or (n_lines,) of Color specs, default: (standard matplotlib color order)
        Color to plot each line(s) and error fill(s) in.
        Can input either a single color spec to use for all lines/fills, or 1 per line/fill pair.
        Can input in any of the ways matplotlib colors are defined (strings, 3-tuples, etc.)

    events : callable or array-like, shape=(n_events,)
        List of event values (eg times) to plot as markers on x-axis
        -or- callable function that will just plot the event markers itself.
        See :func:`plot_markers` for details.

    **kwargs
        Any additional keyword args are interpreted as parameters of :func:`plt.axes`
        (settable Axes object attributes), :func:`plt.plot` (Line2D object attributes),
        or :func:`plt.fill` (Polygon object attributes) and passsed to the proper function.
        A few commonly used options, with custom defaults:

        linewidth : scalar, default: 1.5
            Width of all plotted data line(s)

        alpha : float, range=[0,1], default: 0.25
            Transparency alpha value for plotting all error fill(s).
            1=fully opaque, 0=fully transparent.

    Returns
    -------
    lines : list of Line2D objects
        ax.plot output. Allows access to line properties of line.

    patches : list of Polygon objects
        ax.fill output. Allows access to patch properties of fill.

    ax : Axis object
        Axis plotted into
    """
    x = np.asarray(x)
    data = np.asarray(data)
    if data.ndim == 1: data = data[np.newaxis,:] # Convert 1d (n,) data -> (1,n) to simplify code
    n_lines = data.shape[0]

    assert data.ndim == 2, \
        ValueError("data must be 1-d (or 2-d for multiple lines) (%d-d data given)" % data.ndim)
    assert data.shape[1] == len(x), \
        ValueError("data (%d) and x (%d) should have same length" % (data.shape[1],len(x)))

    if err is not None:
        err = np.asarray(err)
        if err.ndim == 1: err = err[np.newaxis,:]

        assert err.shape[1] == len(x), \
            ValueError("err.shape[1] (%d) and x (%d) should have same length" % (err.shape[1],len(x)))
        assert err.shape[0] in [n_lines,2*n_lines], \
            ValueError("err must be input as (n,) vector or (2*n_lines,n) array of upper;lower errors")

        # Convert errors to 2-sided upper and lower error bounds to simplify code
        if err.shape[0] == n_lines: upper, lower = data+err, data-err
        else:                       upper, lower = err[0::2,:], err[1::2,:]

        ylim = (lower.min(), upper.max())

    else:
        ylim = (data.min(), data.max())

    # Default ylim to data range +/- 5%
    ylim = (ylim[0]-0.05*np.diff(ylim), ylim[1]+0.05*np.diff(ylim))
    xlim = (x.min(),x.max())

    # Set axis to plot into (default to current axis)
    if ax is None: ax = plt.gca()

    # Sort any keyword args to their appropriate plotting object
    axes_args, plot_args, fill_args = _hash_kwargs(kwargs, [AXES_PARAMS, PLOT_PARAMS, FILL_PARAMS])
    # Merge any input parameters with default values
    axes_args = _merge_dicts(dict(xlim=xlim, ylim=ylim), axes_args)
    plot_args = _merge_dicts(dict(linewidth=1.5), plot_args)
    fill_args = _merge_dicts(dict(alpha=0.25), fill_args)

    # Set plotting colors, including defaults
    color = _set_plot_colors(color, n_lines)

    ax.set(**axes_args) # Set axes parameters

    # Plot event markers (if input)
    if events is not None:
        if callable(events):    events()
        else:                   plot_markers(events, axis='x', ax=ax,
                                             xlim=axes_args['xlim'], ylim=axes_args['ylim'])

    # Plot line(s) and error fill(s) if input
    lines = []
    patches = []
    for j in range(n_lines):
        if err is not None:
            patch = ax.fill(np.hstack((x,np.flip(x))),
                            np.hstack((upper[j,:], np.flip(lower[j,:]))),
                            facecolor=color[j], **fill_args)
            patches.append(patch)

        line = ax.plot(x, data[j,:], '-', color=color[j], **plot_args)
        lines.append(line)

    return lines, patches, ax


def plot_heatmap(x, y, data, ax=None, clim=None, events=None, **kwargs):
    """
    Plot 2D data as a heatmap (aka pseudocolor) plot in given axis

    Uses :func:`plt.imshow`

    Parameters
    ----------
    x : array-like, shape=(n_x,)
        Sampling vector for data dimension to be plotted along x-axis

    y : array-like, shape=(n_y,)
        Sampling vector for data dimension to be plotted along y-axis

    data  : ndarray, shape=(n_y,n_x)
        Data to plot on color axis. NOTE: Data array must be 2d,
        with data to be plotted on y-axis the first dimension and the x-axis data 2nd.

    ax : Pyplot Axis object, default: plt.gca() (current axis)
        Axis to plot into.

    clim : array-like, shape=(2,), default: (data.min(),data.max()) (full range of data)
        [low,high] limits of color axis

    events : callable or array-like, shape=(n_events,)
        List of event values (eg times) to plot as markers on x-axis
        -or- callable function that will just plot the event markers itself.
        See :func:`plot_markers` for details.

    **kwargs
        Any additional keyword args are interpreted as parameters of :func:`plt.axes`
        (settable Axes object attributes) or :func:`plt.imshow` (AxesImage object attributes).
        A few commonly used options, with custom defaults:

        cmap  : str | Colormap object. default: 'viridis' (linear dark-blue to yellow colormap)
            Colormap to plot heatmap in, given either as name of matplotlib colormap or custom
            matplotlib.colors.Colormap object instance.

        origin : {'lower','upper'}, default: 'lower'
            Where 1st value in data is plotted along y-axis: 'lower'=bottom, 'upper'=top.

    Returns
    -------
    img : AxesImage object
        Output of ax.imshow(). Allows access to image properties.

    ax : Axis object
        Axis plotted into.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    assert (x.ndim == 1) and (y.ndim == 1), \
        ValueError("`x` and `y` must be 1-dimensional (x ~ %d-d, y ~ %d-d)" % (x.ndim, y.ndim))
    assert data.ndim == 2, ValueError("data must be 2-dimensional (%d-d data given)" % data.ndim)
    assert data.shape == (len(y),len(x)), \
        ValueError("data (%d,%d) must have dimensions (len(y),len(x)) = (%d,%d)" \
                    % (*data.shape,len(y),len(x)))

    # Set axis to plot into (default to current axis)
    if ax is None: ax = plt.gca()
    # Default color range to data min/max
    if clim is None: clim = (data.min(), data.max())

    # Find sampling intervals for x, y axes
    dx = np.diff(x).mean() if len(x) > 1 else 1
    dy = np.diff(y).mean() if len(y) > 1 else 1
    # Set default plotting extent for each axis = full sampling range +/- 1/2 sampling interval
    # This allows for viewing the entire cells at the edges of the plot, which sometimes makes
    # a difference for sparsely sampled dimensions
    xlim = [x[0]-dx/2, x[-1]+dx/2]
    ylim = [y[0]-dy/2, y[-1]+dy/2]

    # Sort any keyword args to their appropriate plotting object
    axes_args, imshow_args, line_args = _hash_kwargs(kwargs,
                                                     [AXES_PARAMS, IMSHOW_PARAMS, PLOT_PARAMS])
    # Merge any input parameters with default values
    axes_args = _merge_dicts(dict(xlim=xlim, ylim=ylim), axes_args)
    imshow_args = _merge_dicts(dict(extent=[*xlim,*ylim], vmin=clim[0], vmax=clim[1],
                                    cmap='viridis', origin='lower', aspect='auto',
                                    interpolation='none'), imshow_args)

    img = ax.imshow(data, **imshow_args)

    ax.set(**axes_args) # Set axes parameters

    # TODO Fix this
    # Have to manually invert y-axis tick labels if plotting w/ origin='upper'
    # if origin == 'upper':
    #     yticks = ax.get_yticks()
    #     idxs = (yticks[0] >= ylim[0]) & (yticks[0] <= ylim[1])
    #     yticks = yticks[0][idxs], np.asarray(yticks[1][idxs])
    #     plt.set_yticks(yticks[0])
    #     plt.set_yticklabels(np.flip(yticks[1]))

    # Plot event markers (if input)
    if events is not None:
        if callable(events):    events()
        else:                   plot_markers(events, axis='x', ax=ax,
                                             xlim=axes_args['xlim'], ylim=axes_args['ylim'],
                                             **line_args)

    return img, ax


def plot_lineseries(x, y, data, ax=None, scale=1.5, color='C0', origin='upper',
                    events=None, **kwargs):
    """
    Plot 2d data as series of vertically-offset line plots with same x-axis values

    Used for example when plotting time-series traces from multiple electrodes on a linear probe.

    Uses :func:`plt.plot`

    Parameters
    ----------
    x : array-like, shape=(n_x,)
        Sampling vector for data dimension to be plotted on x-axis. This will often be timepoints.

    y : array-like, shape=(n_y,)
        Sampling vector for data dimension to be plotted along y-axis. Can be either numeric or
        string labels ot plot for y-axis ticklabels (one at each plotted line).
        This will often be channel numbers or channel labels.

    data : ndarray, shape=(n_y,n_x)
        Data to plot as vertically-offset line series. NOTE: Data array must be 2d,
        with data to be plotted on y-axis the first dimension and the x-axis data 2nd.

    ax :  Pyplot Axis object, default: plt.gca() (current axis)
         Axis to plot into

    scale : float, default: 1.5
        Scale factor for plotting data. 1 = max range of entire data maps to offset between
        successive lines in plot; >1 = extends farther; <1 = scaled smaller than offset.

    color : Color spec | (n_y,) of Color specs, default: 'C0' (blue for all lines)
        Color(s) to use to plot each line in line series.
        Can input either a single color spec to use for all lines/fills, or 1 per line/fill pair.
        Can input in any of the ways matplotlib colors are defined (strings, 3-tuples, etc.)

    origin : {'lower','upper'}, default: 'upper'
        Where 1st value in data is plotted along y-axis;'lower'=bottom, 'upper'=top.
        Default order plots in same order as a probe numbered from topmost contact.

    events : callable or array-like, shape=(n_events,)
        List of event values (eg times) to plot as markers on x-axis
        -or- callable function that will just plot the event markers itself.
        See :func:`plot_markers` for details.

    **kwargs
        Any additional keyword args are interpreted as parameters of :func:`plt.axes`
        (settable Axes object attributes) or :func:`plt.plot` (Line2D object attributes)
        and passsed to the proper function.
        A few commonly used options, with custom defaults:

        linewidth : scalar, default: 1
            Width of all plotted data line

    Returns
    -------
    lines : list of Line2D objects
        ax.plot output. Allows access to line properties of line.

    ax : Axis object
        Axis plotted into.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    data = np.asarray(data)
    n_lines = len(y)

    assert data.ndim == 2, ValueError("data must be 2-dimensional (%d-d data given)" % data.ndim)
    assert data.shape == (len(y),len(x)), \
        ValueError("data (%d,%d) must have dimensions (len(y),len(x)) = (%d,%d)" \
                    % (*data.shape,len(y),len(x)))

    # If y is numeric, use it to plot y-axis; otherwise (eg if string labels) use 0:n_lines-1
    y_plot = y if isnumeric(y) else np.arange(n_lines)

    if ax is None: ax = plt.gca()

    # Sort any keyword args to their appropriate plotting object
    axes_args, plot_args = _hash_kwargs(kwargs, [AXES_PARAMS, PLOT_PARAMS])
    # Merge any input parameters with default values
    xlim = (x.min(),x.max())
    ylim = (y_plot[0]-1,y_plot[-1]+1)
    axes_args = _merge_dicts(dict(xlim=xlim, ylim=ylim), axes_args)
    plot_args = _merge_dicts(dict(linewidth=1), plot_args)
    # Set plotting colors, including defaults
    color = _set_plot_colors(color, n_lines)

    # Scale data so max range of data = <scale>*offset btwn lines on plot
    max_val = np.abs(data).max()
    data = scale * data / max_val

    ax.set(**axes_args) # Set axes parameters

    # Plot event markers (if input)
    if events is not None:
        if callable(events):    events()
        else:                   plot_markers(events, axis='x', ax=ax,
                                             xlim=axes_args['xlim'], ylim=axes_args['ylim'])

    # Plot each line plot (eg channel) in data with appropriate offset
    lines = []
    for j in range(n_lines):
        offset = y_plot[n_lines - (j+1)] if origin == 'upper' else y_plot[j]
        # offset = n_lines - (j+1) if origin == 'upper' else j
        tmp_lines = ax.plot(x, data[j,:] + offset, color=color[j], **plot_args)
        lines.append(tmp_lines)

    ax.set_yticks(y_plot)
    ax.set_yticklabels(y if origin == 'lower' else np.flip(y))

    return lines, ax


# =============================================================================
# Plotting utilities
# =============================================================================
def full_figure(**kwargs):
    """
    Create full-screen figure

    Wrapper around :func:`plt.figure` that sets size to full screen.

    Parameters
    ----------
    **kwargs
        Any keyword args passed directly to :func:`plt.figure`

    Returns
    -------
    fig : Figure object
        Output of :func:`plt.figure`
    """
    if 'frameon' not in kwargs: kwargs.update(frameon=True) # WAS False (changed due to MPL 3.1.0)
    fig = plt.figure(**kwargs)
    _maximize_figure()
    return fig


def savefig(filename, fig=None, figsize=(11.0,8.5), dpi=500, makedir=True, **kwargs):
    """
    Save figure to file in (more-or-less) WYSIWYG manner, generate target directory if missing

    Wrapper around fig.savefig()

    Parameters
    ----------
    filename : str
        Full-path filename to save figure into. If no file extension included, by default
        we add .png (to save a PNG file).

    fig : Pyplot Figure object, default: plt.gcf()
        Figure to save. Defaults to current figure.

    figsize : 2-tuple of float, default: default: (11.0,8.5)
        Figure dimension (width, height) in inches. Defaults to standard 8.5 x 11 in portrait.

    dpi : float, default: 500
        Resolution of saved figure in dots per inch.

    makedir : bool, default, True
        If True, creates requested directory to save figure into if missing

    References
    ----------
    https://stackoverflow.com/questions/45515320/matplotlib-savefig-fullscreen
    """
    if fig is None: fig = plt.gcf()

    # Create full path to save figure file into if doesn't already exist
    path, file = os.path.split(filename)
    if not os.path.exists(path):
        if makedir:
            os.makedirs(path)
        else:
            raise RuntimeError("Directory '%s does not exist. "
                               "Please make it or set `makedir`=True." % path)

    # If filename has no extension, make it PNG by defaults
    _, ext = os.path.splitext(file)
    if ext == '':   filename = filename + '.png'

    # Set size of figure to save and save it
    fig.set_size_inches(figsize, forward=False)
    fig.savefig(filename, dpi=dpi, **kwargs)


def make_colormap(name=None, colors=None, register=None, **kwargs):
    """
    Create a custom colormap and register its name for later convenient use

    Parameters
    ----------
    name : str
        Name of colormap to create. If `register` is True, name will be registered as a
        matplotlib colormap, so later you can invoke it using cmap=`name`.

    colors : callable or dict or array-like
        Specifies the colors in custom colormap in one of three ways:

        (1) callable : `colors` is input as a function/lambda that generates
            `colors` under one of the two following specifications...

        (2) dict : Keys = 'red', 'green', 'blue', and (optionally) 'alpha'.
            Values for each = (n_segments-1,3) array-like of floats in range (0,1). These are
            anchor points for each color, and segments of colormap will be linearly interpolated
            between each to generate a full colormap. The first of the 3 values in each row
            determines where the anchor point lies in the colormap (0-1 ~ lowest to highest point).
            Color segements are interpolated from the 3rd value in one row to the 2nd value in
            the subsequent row (see LinearSegmentedColormap ref below for full explanation).
            Colormap generated using :func:`matplotlib.colors.LinearSegmentedColormap`.

        (3) array-like : List of Matplotlib color specifications, or an equivalent
            (n_colors,3=RGB) or (n_colors,4=RGBA) array. Specifies each color in entire
            colormap. Colormap generated using :func:`matplotlib.colors.ListedColormap`.

    register : bool, default: True if value given for `name`
            If True, `name` is registered as matplotlib colormap, which can later be invoked
            using cmap=`name`.

    **kwargs :
        Any other keyword args passed directly to `LinearSegmentedColormap` or `ListedColormap`.

    Returns
    -------
    cmap : matplotlib.colors.Colormap object (LinearSegmentedColormap or ListedColormap)
        Generated colormap

    References
    ----------
    https://matplotlib.org/stable/tutorials/colors/colormap-manipulation.html
    https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html
    https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.ListedColormap.html
    """
    if register is None: register = name is not None

    # If `colors` input as callable, run it to generate actual colors for colormap
    colors = colors() if callable(colors) else colors

    # If `colors` is dict, we assume it contains points to linearly interp colormap segments btwn
    if isinstance(colors,dict):
        cmap = LinearSegmentedColormap(name=name, segmentdata=colors, **kwargs)

    # If `colors` is array/list, we assume it directly represents all colors in colormap
    elif isarraylike(colors):
        cmap = ListedColormap(colors=colors, name=name, **kwargs)

    else:
        raise TypeError("Unsupported type <%s> set for `colors`" % type(colors))

    # Register colormap name for later use
    if register: plt.register_cmap(cmap=cmap)

    return cmap


def colorbar(mappable=None, ax=None, size=0.05, pad=0.05, **kwargs):
    """
    Create a colorbar for given axis without messing up parent axis size (as plt.colorbar() does)

    Wrapper around `fig.colorbar`

    Parameters
    ----------
    mappable : matplotlib.cm.ScalarMappable object, default: ax._gci() (current artist)
        The thing this colorbar is supposed to describe (eg the output of plt.imshow()).
        Defaults to current colorable artist, if available.

    ax :  Pyplot Axis object, default: plt.gca() (current axis)
         Parent axis to plot colorbar for (eg axis with image/heatmap plot)

    size : float, default: 0.05
        Colorbar width, expressed as proportion of parent axis width

    pad : float, default: 0.05
        Distance of colorbar from parent axis, expressed as proportion of parent axis width

    **kwargs :
        Any other keyword args passed directly to `fig.colorbar`.

    Returns
    -------
    cbar : matplotlib.colorbar.Colorbar object
        Output of plt.colorbar(). Allows customization of colorbar properties.

    References
    ----------
    https://stackoverflow.com/questions/32462881/add-colorbar-to-existing-axis
    """
    # Default: Get the current colorable artist (see pyplot for details)
    if ax is None: ax = plt.gca()
    fig = ax.figure
    if mappable is None: mappable = ax._gci()

    assert mappable is not None, \
        RuntimeError('No mappable was found to use for colorbar creation. '
                     'First define a mappable such as an image (eg with imshow)')

    # Get size/position of parent axis: (x0, y0, width, height)
    bounds = ax.get_position().bounds

    # Make colorbar axis size/position based on base axis
    # x position of left side of colorbar = `pad`*(parent axis width) from right side
    xpos = bounds[0] + bounds[2] + bounds[2]*pad
    # Width of colorbar = `size`*(parent axis width)
    width   = bounds[2]*size

    # Add new axis of given position,size for colorbar
    cax = fig.add_axes([xpos, bounds[1], width, bounds[3]])
    # Create colorbar
    return fig.colorbar(mappable, cax=cax, **kwargs)


def plot_markers(values, axis='x', ax=None, xlim=None, ylim=None,
                 linecolor=[0.50,0.50,0.50], linewidth=0.5,
                 fillcolor=[0.50,0.50,0.50], fillalpha=0.2):
    """
    Plot set of markers on given axis/axes (eg to mark trial event times)

    Single point events should be input as scalars in `values`, and are plotted as
    a single line of given color and width.

    Events extending over a range/duration should be input as 2-length (start,end) tuples,
    in `values`, and are plotted as filled rectangles of given color and alpha (transparency).

    Events that reflect a central value (eg mean) +/- a range or error (eg SDs) should
    be input as 3-length (center-error,center,center+error) tuples in `values`, and are
    plotted as a solid central line with dashed error lines, in the given color and width.

    All marker types extend the full length of the opposing axis.

    NOTE: If limits are explicitly input for the axis the markers are plotted on, any marker fully
    outside of the plot limits will not be plotted, to avoid surprise expansion of the plot limits.

    Parameters
    ----------
    values : array-like, shape=(n_events,), dtype=scalars and/or 2-tuples and/or 3-tuples
        List of values (eg trial event times) on given axes to plot markers for.
        Each entry in list can be a scalar (plotted as a line), a (start,end)
        2-length tuple (plotted as a filled rectangle), or a (-err,center,+err)
        3-length tuple (plotted as solid line with surrounding dashed lines).

    axis : {'x','y','both'}, default: 'x'
        Which axis to plot markers on -- x-axis, y-axis, or both axes (eg for time x time plot)

    Returns
    -------
    ax : Axis object
        Axis plotted into.

    handles : List of Line2D, Polygon, or lists of Line2D objects
        plt.plot/fill outputs for each marker plotted, in the same order as input.
        Allows access to properties of marker lines/fills.
    """
    if isinstance(values,float) or _isint(values): values = [values]
    xlim_input = xlim is not None
    ylim_input = ylim is not None
    if ax is None: ax = plt.gca()
    if xlim is None: xlim = ax.get_xlim()
    if ylim is None: ylim = ax.get_ylim()

    axis = axis.lower()
    assert axis in ['x','y','both'], ValueError("axis must be 'x'|'y'|'both'")
    axes = ['x','y'] if axis == 'both' else [axis]

    # Functions to plot lines or fills for each event in list
    def plot_single_line(value, axis):
        """ Plot scalar value as single line extending the length of the opposing axis """
        if axis == 'x':
            lines = ax.plot([value]*2, ylim, '-', color=linecolor, linewidth=linewidth)
        elif axis == 'y':
            lines = ax.plot(xlim, [value]*2, '-', color=linecolor, linewidth=linewidth)

        return lines

    def plot_fill(value, axis):
        if axis == 'x':
            patches = ax.fill([value[0],value[0],value[1],value[1]],
                              [ylim[0],ylim[1],ylim[1],ylim[0]],
                              color=fillcolor, edgecolor=None, alpha=fillalpha)
        elif axis == 'y':
            patches = ax.fill([xlim[0],xlim[1],xlim[1],xlim[0]],
                              [value[0],value[0],value[1],value[1]],
                              color=fillcolor, edgecolor=None, alpha=fillalpha)

        return patches

    def plot_three_lines(value, axis):
        """ Plot 3-tuple as 3 lines (dash,solid,dash) extending length of the opposing axis """
        lines = [None]*3
        if axis == 'x':
            lines[0] = ax.plot([value[0]]*2, ylim, '--', color=linecolor, linewidth=linewidth)
            lines[1] = ax.plot([value[1]]*2, ylim, '-', color=linecolor, linewidth=linewidth)
            lines[2] = ax.plot([value[2]]*2, ylim, '--', color=linecolor, linewidth=linewidth)
        elif axis == 'y':
            lines[0] = ax.plot(xlim, [value[0]]*2, '--', color=linecolor, linewidth=linewidth)
            lines[1] = ax.plot(xlim, [value[1]]*2, '-', color=linecolor, linewidth=linewidth)
            lines[2] = ax.plot(xlim, [value[2]]*2, '--', color=linecolor, linewidth=linewidth)

        return lines


    # Iterate thru each marker value (eg event time) and plot line or fill marker for it
    handles = []
    for value in values:
        if isinstance(value,float) or _isint(value): value = [value]
        value = np.atleast_1d(value)
        if value.shape[0] == 0: continue

        # Iterate thru axes (if > 1) to plot markers on
        for axis in axes:
            # Skip plotting any markers that are entirely out of axis limits
            # Note: Only do this if axis limits are explicitly input, to avoid user confusion
            if (axis == 'x') and xlim_input:
                if (value < xlim[0]).all() or (value > xlim[1]).all(): continue
            elif (axis == 'y') and ylim_input:
                if (value < ylim[0]).all() or (value > ylim[1]).all(): continue

            # Plot lines if only scalar value (eg single unitary event time)
            if len(value) == 1:     handle = plot_single_line(value, axis)
            # Plot fill if there are 2 values (start,end) (eg event of given range or duration)
            elif len(value) == 2:   handle = plot_fill(value, axis)
            # Plot fill if there are 2 values (start,end) (eg event of given range or duration)
            elif len(value) == 3:   handle = plot_three_lines(value, axis)
            else:
                raise ValueError("Each value in values must be scalar|2-tuple|3-tuple (not len=%d)"
                                % len(value))

            handles.append(handle)

    return ax, handles


# =============================================================================
# Helper functions
# =============================================================================
def _hash_kwargs(args_dict, attr_lists):
    """
    Given a dict of keyword args input into a plotting function, determine which
    are attributes of each of a given set of plot objects (eg Axes, Lines2D, etc.).

    Parameters
    ----------
    args_dict : dict {str:value}
        List of all keyword args (name:value pairs) input into a plotting function

    attr_lists : List of lists
        Set of lists of attributes of plotting objects that keywords args
        may be attributes of. Function matches each args to its proper attribute list
        (and thus, to its corresponding plotting object).

    Returns
    -------
    **hashed_attrs : tuple of dicts {str:value}
        Each dict contains name:value pairs for all keyword args
        corresponding to each attr_list/plotting object (ie 1st output = args
        corresponding to `attr_lists[0]`, 2nd output ~ `attr_lists[1]`, etc.)

        Any keyword args not matched to any `attr_list` will raise an error.
    """
    # Create list of empty dictionaries to hash arguments into
    hashed_attrs = [{} for _ in range(len(attr_lists))]

    # Step thru each key,value pair in arguments dictionary
    for key,value in args_dict.items():
        # Step thru each passed list of object attributes to hash arguments into,
        # determining if key can be found in its attribute list
        found = False
        for i_list,attr_list in enumerate(attr_lists):
            # If we found a match, save k,v pair into corresponding output hashed dict
            # and break out of for att_lists loop
            if key in attr_list:
                hashed_attrs[i_list].update({key:value})
                found = True
                break

        # If we failed to find a match in any attribute list, raise an error
        if found == False:
            raise AttributeError("Incorrect or misspelled variable in keyword args: %s" % key)

    return tuple(hashed_attrs)


def _set_plot_colors(color, n_plot_objects):
    """ Set plotting colors, including defaults and expanding colors to # of plot objects """
    # If no color set, set default = ['C0','C1',...,'CN'] = default matplotlib plotting color order
    if color is None:
        color = ['C'+str(j) for j in range(n_plot_objects)]

    # Otherwise, ensure number of colors matches number of plotting objects, expanding if necessary
    else:
        color = np.atleast_1d(color)
        # If a RBG triplet is input, enclose it in an outer array, to simplify downstream code
        if ((len(color) == 3) and (n_plot_objects != 3)): color = [color]

        # If only 1 color input, replicate it for all plot objects (ie lines,dots,fills,etc.)
        if (len(color) == 1) and (n_plot_objects != 1):
            color = np.tile(color, (n_plot_objects,))
        else:
            assert len(color) == n_plot_objects, \
                ValueError("Color must have one value per plot obect (line/fill/etc)" \
                           " or a single value that is used for all plot objects" \
                           " (%d colors/%d objects)" % (len(color),n_plot_objects))

    return color


def _maximize_figure():
    """
    Maximize size of current Pyplot figure to fill full screen

    References
    ----------
    https://stackoverflow.com/a/32428266
    """
    manager = plt.get_current_fig_manager()

    # Method depends on which Matplotlib backend you are using
    backend = get_backend()
    if 'qt' in backend.lower():     # QT backend
        manager.resize(manager.window.maximumWidth(), manager.window.maximumHeight())
    elif 'tk' in backend.lower():   # TkAgg backend
        manager.resize(*manager.window.maxsize())
    elif 'wx' in backend.lower():   # WX backend
        manager.frame.Maximize(True)
    else:
        warn("Unsupported Matplotlib backend '%s'. Could not maximize figure." % backend)
