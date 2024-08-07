"""
    My numpydoc description of a kind
    of very exhautive numpydoc format docstring.

    Parameters
    ----------
    first : array_like
        the 1st param name `first`
    second :
        the 2nd param
    third : {'value', 'other'}, optional
        the 3rd param, by default 'value'

    Returns
    -------
    string
        a value in a string

    Raises
    ------
    KeyError
        when a key error
    OtherError
        when an other error
"""

import pandas
import numpy
import matplotlib
from matplotlib import pyplot as plt
import seaborn
from scipy import stats as sps
from typing import Literal

# Literal["solar", "view", "both"]

### A collection of types that can be used to make a plot
type datatypes = pandas.DataFrame | pandas.Series | numpy.ndarray | list | tuple | int | float
### A collection of all named matplotlib colors
exec(
    f"type matplotlib_colors_type = Literal{list(matplotlib.colors.CSS4_COLORS.keys())}"
)
### A collection of all linestyles in matplotlib
type matplotlib_linestyles_types = Literal[
    "solid", "dotted", "dashed", "dashdot", "-", ":", "--", "-.", "None", "", ","
] | tuple | None
### A collection of all marker styles in matplotlib
exec(
    f"type matplotlib_markers_type = Literal{list(matplotlib.lines.Line2D.markers.keys())}"
)


### sub-functions for calculating different types of confidence intervals
def extrapolate_quantile_value_linear(v: pandas.Series, q) -> int | float:
    """Linear extrapolation for quantiles greater than 1 or lower than 0"""
    if (q >= 0) and (q <= 1):
        return v.quantile(q)
    elif q > 1:  ## references are the last two points
        return (v.quantile(1) - v.quantile((len(v) - 2) / (len(v) - 1))) / (
            1 - (len(v) - 2) / (len(v) - 1)
        ) * (q - 1) + v.quantile(1)
    ## case q < 0 , references are the first two points
    return (v.quantile(0) - v.quantile((1) / (len(v) - 1))) / (
        0 - (1) / (len(v) - 1)
    ) * (q - 0) + v.quantile(0)


def std_ci(v: pandas.Series, std_multiplier) -> tuple:
    """Upper and lower bounds of the CI based on standard deviation (normal approximation around mean)"""
    return (
        v.mean() - std_multiplier * v.std(),
        v.mean() - std_multiplier * v.std(),
    )


def wald_ci(v: pandas.Series) -> tuple:
    """Upper and lower bounds of the CI based on Wald's binomial approximation"""
    q_low = pandas.Series(
        [
            0.05 - 1.96 / numpy.sqrt(len(v)) * numpy.sqrt(0.05 * (1 - 0.05)),
            0.05 + 1.96 / numpy.sqrt(len(v)) * numpy.sqrt(0.05 * (1 - 0.05)),
        ]
    ).quantile(q=0.25)
    return ()


### A class for drawing a confidence interval in whatever way you prefer, from pre-defined values
### note: this requires matplotlib, matplotlib.pyplot as plt, numpy, pandas, and scipy.stats as sps
class CI_Drawer(object):
    """A class for drawing a confidence interval in whatever way you prefer, from pre-defined values."""

    def __init__(
        self,
        data: pandas.DataFrame | None = None,  # ok
        x: str | datatypes | None = None,  # ok
        y: str | datatypes | None = None,  # ok
        ci_low: str | datatypes | None = None,  # partial?
        ci_high: str | datatypes | None = None,  # partial?
        ci_type: Literal[
            "std", "Wald", "Wilson", "Clopper–Pearson", "Agresti–Coull", "Rule of three"
        ] = "std",  # ongoing
        extrapolation_type: Literal[
            "linear"
        ] = "linear",  ### TODO: add more options, such as Scholz, Hutson, etc.
        std: str | datatypes | None = None,  # ongoing
        std_multiplier: int | float = 1.96,  # ok (nothing to do?)
        ci_orientation: Literal["horizontal", "vertical"] = "vertical",
        ci_draw_lines: bool = False,  # ok
        ci_draw_line_low: bool | None = None,  # ok
        ci_draw_line_high: bool | None = None,  # ok
        ci_lines_style: matplotlib_linestyles_types = "solid",  # ok
        ci_line_low_style: matplotlib_linestyles_types | None = None,  # ok
        ci_line_high_style: matplotlib_linestyles_types | None = None,  # ok
        ci_lines_color: matplotlib_colors_type = "black",  # ok
        ci_line_low_color: matplotlib_colors_type | None = None,  # ok
        ci_line_high_color: matplotlib_colors_type | None = None,  # ok
        ci_lines_linewidth: int | float = 1,  # ok
        ci_line_low_linewidth: int | float | None = None,  # ok
        ci_line_high_linewidth: int | float | None = None,  # ok
        ci_lines_alpha: int | float = 0.8,  # ok
        ci_line_low_alpha: int | float | None = None,  # ok
        ci_line_high_alpha: int | float | None = None,  # ok
        ci_draw_bars: bool = False,  # ok
        ci_draw_bar_ends: bool | None = None,  # ok
        ci_bars_style: matplotlib_linestyles_types = "solid",  # ok
        ci_bars_color: matplotlib_colors_type = "black",  # ok
        ci_bars_linewidth: int | float = 1,  # ok
        ci_bars_alpha: int | float = 1,  # ok
        ci_bar_ends_style: matplotlib_linestyles_types = "solid",  # ok
        ci_bar_ends_color: matplotlib_colors_type | None = None,  # ok
        ci_bar_ends_width: int | float | None = None,
        ci_bar_ends_ratio: int | float | None = 0.4,
        ci_bar_hide_center_portion: bool = False,
        ci_bar_center_portion_length: int | float | None = None,
        ci_bar_center_portion_ratio: int | float | None = 0.5,
        ci_fill_area: bool = True,
        ci_fill_color: matplotlib_colors_type = "lavender",
        ci_fill_alpha: int | float = 0.4,
        ci_plot_limits: bool = False,  # ok
        ci_plot_low_limit: bool | None = None,  # ok
        ci_plot_high_limit: bool | None = None,  # ok
        ci_plot_markers: matplotlib_markers_type | None = None,  # ok
        ci_plot_low_marker: matplotlib_markers_type | None = None,  # ok
        ci_plot_high_marker: matplotlib_markers_type | None = None,  # ok
        ci_plot_color: matplotlib_colors_type = "black",  # ok
        ci_plot_low_color: matplotlib_colors_type | None = None,  # ok
        ci_plot_high_color: matplotlib_colors_type | None = None,  # ok
        ci_plot_alpha: int | float = 0.8,  # ok
        ci_plot_low_alpha: int | float | None = None,  # ok
        ci_plot_high_alpha: int | float | None = None,  # ok
        ci_plot_size: int | float | None = None,  # ok
        ci_plot_low_size: int | float | None = None,  # ok
        ci_plot_high_size: int | float | None = None,  # ok
        binomial_ci_policy: (
            Literal[
                "conservative",
                "conservative quartile",
                "median",
                "optimistic quartile",
                "optimistic",
            ]
            | int
            | float
        ) = "conservative",  # ok
        ax: matplotlib.axes.Axes | None = None,  # ok
    ):
        ###
        #############################################################################
        ### Argument handling: type check and guessed values
        #############################################################################
        ###
        ### convert binomial_ci_policy to a numeral if it is given as a string
        if isinstance(binomial_ci_policy, str):
            if binomial_ci_policy in self.binomial_ci_policy_dict:
                binomial_ci_policy = self.binomial_ci_policy_dict[binomial_ci_policy]
            else:
                raise ValueError(
                    "'binomial_ci_policy' preset should be one of 'conservative', 'conservative quartile', 'median', optimistic quartile', 'optimistic'."
                )
        elif isinstance(binomial_ci_policy, type(int)) or isinstance(
            binomial_ci_policy, type(float)
        ):
            ### check that the numerical value is between 0 and 1
            if (binomial_ci_policy < 0) or (binomial_ci_policy > 1):
                raise ValueError(
                    "'binomial_ci_policy' should be between 0 (conservative) and 1 (optimistic) if given as a numerical value."
                )
        else:
            raise TypeError(
                "'binomial_ci_policy' should be a numerical value between 0 and 1, or one of 'conservative', 'conservative quartile', 'median', optimistic quartile', 'optimistic'."
            )
        ### check matplotlib axes on which to draw
        if isinstance(ax, type(None)):
            ax = plt.gca()
        ### check all optional arguments with None as default value
        ### case where data is provided as a pandas DataFrame
        if isinstance(data, pandas.DataFrame):
            ### check variables that could have been declared as a column name from data
            ### replace them with the numerical series they refer to
            if isinstance(x, str):
                x = data[x].copy()
            ### if x and/or y have not been declared, look for the names 'x' and 'y' in data,
            ### or assume they are the first and second columns, respectively
            elif isinstance(x, type(None)):
                if "x" in data.columns:
                    x = data["x"].copy()
                elif len(data.columns) == 1:
                    ### special case: if data only contains one column, use the index for x
                    x = data.index.copy()
                elif len(data.columns) >= 2:
                    x = data[data.columns[0]].copy()
                else:
                    raise ValueError(
                        "x can only be implicit if 'data' has at least 1 column."
                    )
            if isinstance(y, str):
                y = data[y].copy()
            elif isinstance(y, type(None)):
                if "y" in data.columns:
                    y = data["y"].copy()
                elif len(data.columns) == 1:
                    ### special case: if data only contains one column, assume that column is y
                    y = data[data.columns[0]].copy()
                elif len(data.columns) >= 2:
                    y = data[data.columns[1]].copy()
                else:
                    raise ValueError(
                        "y can only be implicit if 'data' has at least 1 column."
                    )
            if isinstance(std, str):
                std = data[std].copy()
            if isinstance(ci_low, str):
                ci_low = data[ci_low].copy()
            if isinstance(ci_high, str):
                ci_high = data[ci_high].copy()
        else:
            ### if numerical values as first argument instead of data, take them as y
            if isinstance(
                data,
                (
                    pandas.Series,
                    numpy.ndarray,
                    type(list),
                    type(tuple),
                    type(int),
                    type(float),
                ),
            ):
                y = data
            ### check variables that could have WRONGLY been declared as a column name from data without any data...
            if isinstance(x, str):
                raise TypeError(
                    "'x' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            if isinstance(y, str):
                raise TypeError(
                    "'y' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            elif isinstance(y, type(None)):
                raise ValueError("If 'data' is not provided, 'y' must be provided.")
            if isinstance(std, str):
                raise TypeError(
                    "'std' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            if isinstance(ci_low, str):
                raise TypeError(
                    "'ci_low' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            if isinstance(ci_high, str):
                raise TypeError(
                    "'ci_high' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            ### TODO: add a condition to catch any numerical value passed as first argument, and save it as y unless y was specified
        ###
        #############################################################################
        ### Argument handling: type checking for x, y, data, and calculations
        #############################################################################
        ###
        ### Ensure the compatible formating of x and y numerical series
        y = pandas.Series(y)
        if isinstance(x, type(None)):
            x = y.index
        x = pandas.Series(x)
        ### TODO: add a check for te equal length of x and y if they were not provided as part of a dataframe
        ### check if at least one of std, ci_low, or ci_high was provided
        if (
            isinstance(std, type(None))
            and isinstance(ci_low, type(None))
            and isinstance(ci_high, type(None))
        ):
            # raise ValueError("At least one of 'std', 'ci_low', or 'ci_high' must be provided.")
            ### estimate the value of std based on the variability of y for each value of x
            ### TODO: solve the error raised when data is not provided... Reconstitute from y?
            s = pandas.Series([y.loc[x == val_x].std() for val_x in x.unique()]).fillna(
                0
            )
        ### TODO; if std was provided, use it to calculate ci_low and ci_high
        ci_low = pandas.Series(ci_low)
        ci_high = pandas.Series(ci_high)
        ###
        #############################################################################
        ### Argument handling: boolean checks and defaults for optional arguments
        #############################################################################
        ###
        ### TODO: implement toggles such as ci_draw_lines, etc.
        ### if "sub" variables are None, they take the value of the "master" variable
        ### draw_lines
        if isinstance(ci_draw_line_low, type(None)):
            ci_draw_line_low = ci_draw_lines
        if isinstance(ci_draw_line_high, type(None)):
            ci_draw_line_high = ci_draw_lines
        ### lines_style
        if isinstance(ci_line_low_style, type(None)):
            ci_line_low_style = ci_lines_style
        if isinstance(ci_line_high_alpha, type(None)):
            ci_line_high_style = ci_lines_style
        ### lines_color
        if isinstance(ci_line_low_color, type(None)):
            ci_line_low_color = ci_lines_color
        if isinstance(ci_line_high_color, type(None)):
            ci_line_high_color = ci_lines_color
        ### lines_linewidth
        if isinstance(ci_line_low_linewidth, type(None)):
            ci_line_low_linewidth = ci_lines_linewidth
        if isinstance(ci_line_high_linewidth, type(None)):
            ci_line_high_linewidth = ci_lines_linewidth
        ### lines_alpha
        if isinstance(ci_line_low_alpha, type(None)):
            ci_line_low_alpha = ci_lines_alpha
        if isinstance(ci_line_high_alpha, type(None)):
            ci_line_high_alpha = ci_lines_alpha
        ### draw_bar_ends
        if isinstance(ci_draw_bar_ends, type(None)):
            ci_draw_bar_ends = ci_draw_bars
        ### bar_ends_color
        if isinstance(ci_bar_ends_color, type(None)):
            ci_bar_ends_color = ci_bars_color
        ### plot_limits
        if isinstance(ci_plot_low_limit, type(None)):
            ci_plot_low_limit = ci_plot_limits
        if isinstance(ci_plot_high_limit, type(None)):
            ci_plot_high_limit = ci_plot_limits
        ### plot_markers
        if isinstance(ci_plot_low_marker, type(None)):
            ci_plot_low_marker = ci_plot_markers
        if isinstance(ci_plot_high_marker, type(None)):
            ci_plot_high_marker = ci_plot_markers
        ### plot_color
        if isinstance(ci_plot_low_color, type(None)):
            ci_plot_low_color = ci_plot_color
        if isinstance(ci_plot_high_color, type(None)):
            ci_plot_high_color = ci_plot_color
        ### plot_size
        if isinstance(ci_plot_low_size, type(None)):
            ci_plot_low_size = ci_plot_size
        if isinstance(ci_plot_high_size, type(None)):
            ci_plot_high_size = ci_plot_size
        ### plot_alpha
        if isinstance(ci_plot_low_alpha, type(None)):
            ci_plot_low_alpha = ci_plot_alpha
        if isinstance(ci_plot_high_alpha, type(None)):
            ci_plot_high_alpha = ci_plot_alpha
        ###
        #############################################################################
        ### Instance preparation: saving variables and parameters
        #############################################################################
        ###
        ### TODO: would it be better to save the instance variables AFTER checking them?
        self.data = data
        self.x = x
        self.y = y
        self.ci_low = ci_low
        self.ci_high = ci_high
        self.std = std
        ### Save all toggles in a dictionary
        self.params = {
            "ci_type": ci_type,
            "extrapolation_type": extrapolation_type,
            "std_multiplier": std_multiplier,
            "ci_orientation": ci_orientation,  ## TODO: implement the case where the CI is horizintal (i.e., on the x axis)
            # "ci_draw_lines": ci_draw_lines,  ## currently not needed, but kept as comment for now in case it would be needed later
            "ci_draw_line_low": ci_draw_line_low,
            "ci_draw_line_high": ci_draw_line_high,
            # "ci_lines_style": ci_lines_style,
            "ci_line_low_style": ci_line_low_style,
            "ci_line_high_style": ci_line_high_style,
            # "ci_lines_color": ci_lines_color,
            "ci_line_low_color": ci_line_low_color,
            "ci_line_high_color": ci_line_high_color,
            # "ci_lines_linewidth": ci_lines_linewidth,
            "ci_line_low_linewidth": ci_line_low_linewidth,
            "ci_line_high_linewidth": ci_line_high_linewidth,
            # "ci_lines_alpha": ci_lines_alpha,
            "ci_line_low_alpha": ci_line_low_alpha,
            "ci_line_high_alpha": ci_line_high_alpha,
            "ci_draw_bars": ci_draw_bars,
            "ci_draw_bar_ends": ci_draw_bar_ends,
            "ci_bars_style": ci_bars_style,
            "ci_bars_color": ci_bars_color,
            "ci_bars_linewidth": ci_bars_linewidth,
            "ci_bars_alpha": ci_bars_alpha,
            "ci_bar_ends_style": ci_bar_ends_style,
            "ci_bar_ends_color": ci_bar_ends_color,
            "ci_bar_ends_width": ci_bar_ends_width,
            "ci_bar_ends_ratio": ci_bar_ends_ratio,
            "ci_bar_hide_center_portion": ci_bar_hide_center_portion,
            "ci_bar_center_portion_length": ci_bar_center_portion_length,
            "ci_bar_center_portion_ratio": ci_bar_center_portion_ratio,
            "ci_fill_area": ci_fill_area,
            "ci_fill_color": ci_fill_color,
            "ci_fill_alpha": ci_fill_alpha,
            # "ci_plot_limits": ci_plot_limits,
            "ci_plot_low_limit": ci_plot_low_limit,
            "ci_plot_high_limit": ci_plot_high_limit,
            # "ci_plot_markers": ci_plot_markers,
            "ci_plot_low_marker": ci_plot_low_marker,
            "ci_plot_high_marker": ci_plot_high_marker,
            # "ci_plot_color": ci_plot_color,
            "ci_plot_low_color": ci_plot_low_color,
            "ci_plot_high_color": ci_plot_high_color,
            # "ci_plot_alpha": ci_plot_alpha,
            "ci_plot_low_alpha": ci_plot_low_alpha,
            "ci_plot_high_alpha": ci_plot_high_alpha,
            # "ci_plot_size": ci_plot_size,
            "ci_plot_low_size": ci_plot_low_size,
            "ci_plot_high_size": ci_plot_high_size,
            "binomial_ci_policy": binomial_ci_policy,
        }
        self.ax = ax  # ok
        ### TODO: finish registering the variables, including calculated ones
        ###
        #############################################################################
        ### Instance preparation: method call(s) upon initialization
        #############################################################################
        ###
        self.draw()

    def __call__(self):
        pass

    ### dictionary for binomial_ci_policy
    binomial_ci_policy_dict = {
        "conservative": 0,
        "conservative quartile": 0.25,
        "median": 0.5,
        "optimistic quartile": 0.75,
        "optimistic": 1,
    }

    def help():
        print("A help message")

    def draw(self) -> None:  ## return ax instead? Or None?
        ### draw CI lines
        if self.params["ci_draw_line_low"] == True:
            seaborn.lineplot(
                x=self.x,
                y=self.ci_low,
                color=self.params["ci_line_low_color"],
                linestyle=self.params["ci_line_low_style"],
                linewidth=self.params["ci_line_low_linewidth"],
                alpha=self.params["ci_line_low_alpha"],
            )
        if self.params["ci_draw_line_high"] == True:
            seaborn.lineplot(
                x=self.x,
                y=self.ci_high,
                color=self.params["ci_line_high_color"],
                linestyle=self.params["ci_line_high_style"],
                linewidth=self.params["ci_line_high_linewidth"],
                alpha=self.params["ci_line_high_alpha"],
            )
        ### draw ci bars
        if self.params["ci_draw_bars"] == True:
            plt.vlines(
                x=self.x,
                ymin=self.ci_low,
                ymax=self.ci_high,
                color=self.params["ci_bars_color"],
                linestyles=self.params["ci_bars_style"],
                linewidth=self.params["ci_bars_linewidth"],
                alpha=self.params["ci_bars_alpha"],
            )
            if self.params["ci_draw_bar_ends"] == True:
                ci_ends_width = (
                    (numpy.max(self.x) - numpy.min(self.x) + 1) / len(self.x) * 0.4
                )  ## self.params['ci_bar_ends_width']
                plt.hlines(
                    y=self.ci_low,
                    xmin=self.x - ci_ends_width / 2,
                    xmax=self.x + ci_ends_width / 2,
                    color=self.params["ci_bar_ends_color"],
                    linestyles=self.params["ci_bar_ends_style"],
                    linewidth=self.params["ci_bars_linewidth"],
                    alpha=self.params["ci_bars_alpha"],
                )
                plt.hlines(
                    y=self.ci_high,
                    xmin=self.x - ci_ends_width / 2,
                    xmax=self.x + ci_ends_width / 2,
                    color=self.params["ci_bar_ends_color"],
                    linestyles=self.params["ci_bar_ends_style"],
                    linewidth=self.params["ci_bars_linewidth"],
                    alpha=self.params["ci_bars_alpha"],
                )
        ### fill CI area
        if self.params["ci_fill_area"] == True:
            plt.fill_between(
                x=self.x,
                y1=self.ci_low,
                y2=self.ci_high,
                color=self.params["ci_fill_color"],
                alpha=self.params["ci_fill_alpha"],
            )

        ### scatterplot of CI limits
        if self.params["ci_plot_low_limit"] == True:
            seaborn.scatterplot(
                x=self.x,
                y=self.ci_low,
                color=self.params["ci_plot_low_color"],
                size=self.params["ci_plot_low_size"],
                markers=self.params["ci_plot_low_marker"],
                alpha=self.params["ci_plot_low_alpha"],
            )
        if self.params["ci_plot_high_limit"] == True:
            seaborn.scatterplot(
                x=self.x,
                y=self.ci_high,
                color=self.params["ci_plot_high_color"],
                size=self.params["ci_plot_high_size"],
                markers=self.params["ci_plot_high_marker"],
                alpha=self.params["ci_plot_high_alpha"],
            )
        # ### scatterplot
        # seaborn.scatterplot(
        #     data=newdata,
        #     x=newdata.index,
        #     y="y mean",
        #     hue="origin cluster",
        #     palette="rainbow_r",
        #     marker=".",
        #     s=100,
        #     alpha=1,
        # )
