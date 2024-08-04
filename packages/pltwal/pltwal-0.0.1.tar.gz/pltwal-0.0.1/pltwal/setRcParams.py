"""
Creates a matplotlib cmap from the currently used pywal colorscheme
"""

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib as mpl
import re
from os import getenv

with open(getenv("HOME") + "/.cache/wal/colors.sh", "r") as f:
    walstring = f.read()

colors = re.findall("""color\d{1,2}='(#.{6})'""", walstring)
background = re.findall("""background='(#.{6})'""", walstring)[0]
foreground = re.findall("""foreground='(#.{6})'""", walstring)[0]

colorsReduced = colors[1:7] + colors[9:15]

plt.rcParams["axes.facecolor"] = background
plt.rcParams["axes.edgecolor"] = foreground
plt.rcParams["axes.titlecolor"] = foreground
plt.rcParams["axes.labelcolor"] = foreground

plt.rcParams["axes3d.xaxis.panecolor"] = foreground
plt.rcParams["axes3d.yaxis.panecolor"] = foreground
plt.rcParams["axes3d.zaxis.panecolor"] = foreground

"""
plt.rcParams['boxplot.boxprops.color'] = foreground
plt.rcParams['boxplot.capprops.color'] = foreground
plt.rcParams['boxplot.flierprops.color'] = foreground
plt.rcParams['boxplot.flierprops.markeredgecolor'] = foreground
plt.rcParams['boxplot.flierprops.markerfacecolor'] = background
plt.rcParams['boxplot.meanprops.color'] = foreground
plt.rcParams['boxplot.meanprops.markeredgecolor'] = foreground
plt.rcParams['boxplot.meanprops.markerfacecolor'] = background

"""


plt.rcParams["figure.facecolor"] = background
plt.rcParams["figure.edgecolor"] = foreground

plt.rcParams["grid.color"] = colors[7]
plt.rcParams["hatch.color"] = colors[7]

plt.rcParams["legend.edgecolor"] = foreground
plt.rcParams["legend.facecolor"] = background
plt.rcParams["legend.labelcolor"] = foreground

plt.rcParams["lines.color"] = colors[1]

plt.rcParams["text.color"] = foreground
plt.rcParams["xtick.color"] = foreground
plt.rcParams["xtick.labelcolor"] = foreground
plt.rcParams["ytick.color"] = foreground
plt.rcParams["ytick.labelcolor"] = foreground

plt.rcParams["axes.prop_cycle"] = mpl.cycler(color=colorsReduced)

cmapwal = ListedColormap(colors[1:7], name="wal")
mpl.colormaps.register(cmap=cmapwal)
plt.rcParams["image.cmap"] = "wal"
