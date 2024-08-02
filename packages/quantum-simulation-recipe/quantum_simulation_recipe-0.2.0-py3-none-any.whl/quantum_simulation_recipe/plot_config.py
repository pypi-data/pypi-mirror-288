import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from matplotlib.colors import ListedColormap
import colorsys

SMALL_SIZE = 14
MEDIUM_SIZE = 18  #default 10
LARGE_SIZE = 24
# MARKER_SIZE = 10

plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=LARGE_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=LARGE_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=LARGE_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=LARGE_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize
plt.rc('figure', titlesize=LARGE_SIZE)  # fontsize of the figure title

mpl.rcParams['font.family'] = 'sans-serif'  # 'Helvetica'
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams["xtick.direction"] = 'out' # 'out'
mpl.rcParams["ytick.direction"] = 'out'
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['ytick.major.width'] = 1.5
mpl.rcParams['ytick.minor.width'] = 1.5
mpl.rcParams['lines.markersize'] = 11
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['lines.linewidth'] = 1.5
# plt.rcParams['lines.markeredgecolor'] = 'k'
mpl.rcParams['lines.markeredgewidth'] = 1.5
mpl.rcParams['figure.dpi'] = 100
mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['figure.autolayout'] = True
mpl.rcParams['axes.grid'] = True
mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.transparent'] = True


# Function to lighten a color
def lighten_color(color, amount=0.3):
    # Convert color from hexadecimal to RGB
    if isinstance(color, str):
        r, g, b, a = tuple(int(color[i:i+2], 16) for i in (1, 3, 5, 7))
    else:
        r, g, b, a = color
        if 0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1 and 0 <= a <= 1:
            r, g, b, a = int(r*255), int(g*255), int(b*255), int(a*255)
        else: 
            raise ValueError('Color should be in hexadecimal or RGB format')
    # print(r, g, b, a)
    # Convert RGB to HLS
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    # Lighten the luminance component
    l = min(1, l + amount)
    # Convert HLS back to RGB
    r, g, b = tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, l, s))
    # Convert RGB back to hexadecimal
    new_color = f"#{r:02x}{g:02x}{b:02x}{a:02x}"
    return new_color

def set_color_cycle(color_cycle, alpha=0.3, mfc=False, edgecolor=False):
    color_cycle_light = [lighten_color(color, alpha) for color in color_cycle]
    if mfc:
        colors = mpl.cycler(mfc=color_cycle_light, color=color_cycle, markeredgecolor=color_cycle)
    else:
        if edgecolor:
            colors = mpl.cycler(color=color_cycle, markeredgecolor=color_cycle)
        else:
            colors = mpl.cycler(color=color_cycle, markeredgecolor=['k']*len(color_cycle))
    mpl.rc('axes', prop_cycle=colors)

default_color_cycle = ["#B65655FF", "#5471abFF", "#6aa66eFF", "#A66E6AFF"]
# set_color_cycle(default_color_cycle)
# mpl.rc('axes', grid=True, edgecolor='k', prop_cycle=colors)
# mpl.rcParams['axes.prop_cycle'] = colors
# mpl.rcParams['lines.markeredgecolor'] = 'C'

from colorspace import sequential_hcl
class GradColors:
    def __init__(self, rate_num):
        self.rate_num = rate_num
        # https://colorspace.r-forge.r-project.org/reference/hcl_palettes.html
        self.purple = mpl.colors.ListedColormap(sequential_hcl("Purples")(rate_num+1)[:-1][::-1], name='from_list', N=None) 
        self.red = mpl.colors.ListedColormap(sequential_hcl("Reds")(rate_num+1)[:-1][::-1], name='from_list', N=None) 
        self.green = mpl.colors.ListedColormap(sequential_hcl("Greens")(rate_num+1)[:-1][::-1], name='from_list', N=None) 
        self.blue = mpl.colors.ListedColormap(sequential_hcl("Blues")(rate_num+1)[:-1][::-1], name='from_list', N=None) 
        self.orange = mpl.colors.ListedColormap(sequential_hcl("Oranges")(rate_num+1)[:-1][::-1], name='from_list', N=None) 
        self.mint = mpl.colors.ListedColormap(sequential_hcl("Mint")(rate_num+1)[:-1][::-1], name='from_list', N=None)
        # self.return_colors()

    def get_colors(self, c: str):
        return mpl.colors.ListedColormap(sequential_hcl(c)(self.rate_num+1)[:-1][::-1], name='from_list', N=None) 


from scipy.optimize import curve_fit
from math import ceil, floor, log, exp

def linear_loglog_fit(x, y, verbose=False):
    # Define the linear function
    def linear_func(x, a, b):
        return a * x + b

    log_x = np.array([log(n) for n in x])
    log_y = np.array([log(cost) for cost in y])
    # Fit the linear function to the data
    params, covariance = curve_fit(linear_func, log_x, log_y)
    # Extract the parameters
    a, b = params
    # Predict y values
    y_pred = linear_func(log_x, a, b)
    # Print the parameters
    if verbose: print('Slope (a):', a, '; Intercept (b):', b)
    exp_y_pred = [exp(cost) for cost in y_pred]

    return exp_y_pred, a, b

def plot_fit(ax, x, y, var='t', x_offset=1.07, y_offset=1.0, label='', ext_x=[], linestyle='k--', linewidth=1.5, fontsize=MEDIUM_SIZE, verbose=True):
    y_pred_em, a_em, b_em = linear_loglog_fit(x, y)
    if verbose: print(f'a_em: {a_em}; b_em: {b_em}')
    if abs(a_em) < 1e-3: 
        text_a_em = "{:.2f}".format(round(abs(a_em), 4))
    else:
        text_a_em = "{:.2f}".format(round(a_em, 4))

    if ext_x != []: x = ext_x
    y_pred_em = [exp(cost) for cost in a_em*np.array([log(n) for n in x]) + b_em]
    if label =='':
        ax.plot(x, y_pred_em, linestyle, linewidth=linewidth)
    else:
        ax.plot(x, y_pred_em, linestyle, linewidth=linewidth, label=label)
    ax.annotate(r'$O(%s^{%s})$' % (var, text_a_em), xy=(x[-1], np.real(y_pred_em)[-1]), xytext=(x[-1]*x_offset, np.real(y_pred_em)[-1]*y_offset), fontsize=fontsize)

    return a_em, b_em

def ax_set_text(ax, x_label, y_label, title=None, legend='best', xticks=None, yticks=None, grid=None, log='', ylim=None):
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if title: ax.set_title(title)
    if legend: ax.legend(loc=legend)

    if log == 'x': 
        ax.set_xscale('log')
    elif log == 'y':
        ax.set_yscale('log')
    elif log == 'xy':
        # ax.set_xscale('log')
        # ax.set_yscale('log')
        ax.loglog()
    else:
        pass

    if grid: ax.grid()  
    if ylim: ax.set_ylim([ylim[0]*0.85, ylim[1]*1.15])

    if xticks is not None: 
        ax.set_xticks(xticks)
        ax.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

    if yticks is not None: 
        ax.set_yticks(yticks)
        ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

# def data_plot(x, y, marker, label, alpha=1, linewidth=1, loglog=True, markeredgecolor='black'):
#     if loglog:
#         plt.loglog(x, y, marker, label=label, linewidth=linewidth, markeredgecolor=markeredgecolor, markeredgewidth=0.5, alpha=alpha)
#     else:
#         plt.plot(x, y, marker, label=label, linewidth=linewidth, markeredgecolor=markeredgecolor, markeredgewidth=0.5, alpha=alpha)

def plot_evo(ax, t_list, y_list, marker, color='', title='', xlabel='', ylabel='', label='', markersize=10, markeredgewidth=1.5, lw=1.5, inset=False):
    if color == '':
        ax.plot(t_list, y_list, marker, label=label, markersize=markersize, markeredgewidth=markeredgewidth, linewidth=lw)
        # ax.plot(t_list, y_list, '-', markersize=5)
        # ax.plot(t_list, y_list, 'o', label=label, markersize=5)
        # ax.plot(t_list, y_list, marker, label=label, markeredgecolor='k', markeredgewidth=0.4, markersize=5)
    else:
        ax.plot(t_list, y_list, marker, color=color, label=label, markeredgecolor=color, markeredgewidth=markeredgewidth, markersize=markersize, linewidth=lw, mfc=lighten_color(color, 0.3))
        # ax.plot(t_list, y_list, marker, color=color, label=label, markeredgecolor=color, markeredgewidth=0.4, markersize=markersize, mfc=color[:-2]+"80")
    if not inset: 
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    if title  != '': ax.set_title(title)
    if xlabel != '': 
        ax.set_xlabel(xlabel)
    # else:
    #     ax.set_xticks([]) 
    if ylabel != '': ax.set_ylabel(ylabel)
    # else:
    #     ax.set_xticks([])

def letter_annotation(axes, x_offset, y_offset, letters, fontsize=14):
    # https://towardsdatascience.com/a-guide-to-matplotlib-subfigures-for-creating-complex-multi-panel-figures-70fa8f6c38a4
    for letter in letters:
        axes[letter].text(x_offset, y_offset, f'({letter})', transform=axes[letter].transAxes, size=fontsize, weight='bold')


def matrix_plot(M):
    fig, ax = plt.subplots()
    real_matrix = np.real(M)
    # Plot the real part using a colormap
    ax.imshow(real_matrix, cmap='RdYlBu', interpolation='nearest', origin='upper')
    # Create grid lines
    ax.grid(True, which='both', color='black', linewidth=1)
    # Add color bar for reference
    cbar = plt.colorbar(ax.imshow(real_matrix, cmap='RdYlBu', interpolation='nearest', origin='upper'), ax=ax, orientation='vertical')
    cbar.set_label('Real Part')
    # Add labels to the x and y axes
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    # Show the plot
    plt.title('Complex Matrix with Grid')
    plt.show()