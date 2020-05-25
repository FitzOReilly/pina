from matplotlib import pyplot as plt

from pinch.stream import make_stream, make_segmented_stream
from pinch.stream_analyzer import StreamAnalyzer


# Some customizations to make the plots pretty
FIGSIZE = (16, 7)
HCC_STYLE = {
    "color": "tab:red",
    "linestyle": "--",
    "label": "HCC",
}
CCC_STYLE = {
    "color": "tab:blue",
    "linestyle": "-",
    "label": "CCC",
}
GCC_STYLE = {
    "color": "k",
    "linestyle": "-",
    "label": "GCC",
}


def summary(stream_analyzer):
    """
    Returns a string with the energy targets and the pinch temperature(s).
    """
    return (
        "Heating demand: {0:0.2f}\n"
        "Cooling demand: {1:0.2f}\n"
        "Hot utility target: {2:0.2f}\n"
        "Cold utility target: {3:0.2f}\n"
        "Heat recovery target: {4:0.2f}\n"
        "Pinch temperature(s): {5}\n"
        .format(
            stream_analyzer.heating_demand,
            stream_analyzer.cooling_demand,
            stream_analyzer.hot_utility_target,
            stream_analyzer.cold_utility_target,
            stream_analyzer.heat_recovery_target,
            stream_analyzer.pinch_temps
        )
    )


def plot_results(stream_analyzer, param_dict):
    """
    Creates two plots: One of the hot and cold composite curves and one of the
    grand composite curve. Returns a tuple with the figure and axes objects.
    """
    fig, ax = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.suptitle(param_dict["title"], fontweight="bold")

    ax[0].plot(*stream_analyzer.hot_composite_curve, **param_dict["hcc_style"])
    ax[0].plot(*stream_analyzer.cold_composite_curve, **param_dict["ccc_style"])
    ax[0].legend()
    ax[0].set_title(param_dict["hcc_ccc_title"])
    ax[0].set_xlabel(param_dict["hcc_ccc_xlabel"])
    ax[0].set_ylabel(param_dict["hcc_ccc_ylabel"])

    ax[1].plot(*stream_analyzer.grand_composite_curve, **param_dict["gcc_style"])
    ax[1].legend()
    ax[1].set_title(param_dict["gcc_title"])
    ax[1].set_xlabel(param_dict["gcc_xlabel"])
    ax[1].set_ylabel(param_dict["gcc_ylabel"])

    # Make the y-axis equal in both plots
    ylims = (*ax[0].get_ylim(), *ax[1].get_ylim())
    minmax_ylims = (min(ylims), max(ylims))
    ax[0].set_ylim(minmax_ylims)
    ax[1].set_ylim(minmax_ylims)

    return fig, ax


def four_stream():
    # Four stream example from
    # Pinch Analysis and Process Integration:
    # A User Guide On Process Integration for the Efficient Use of Energy,
    # Second edition, Ian C. Kemp, page 4
    param_dict = {
        "title": "Four stream example",
        "hcc_ccc_title": "Hot and cold composite curves",
        "hcc_ccc_xlabel": "Heat flow [kW]",
        "hcc_ccc_ylabel": "Actual temperature [\u2103]",
        "gcc_title": "Grand composite curve",
        "gcc_xlabel": "Net heat flow [kW]",
        "gcc_ylabel": "Shifted temperature [\u2103]",
        "hcc_style": HCC_STYLE,
        "ccc_style": CCC_STYLE,
        "gcc_style": GCC_STYLE,
    }

    min_temp_diff = 10
    default_temp_shift = min_temp_diff / 2

    streams = [
        make_stream(-230, 20, 135),
        make_stream(330, 170, 60),
        make_stream(-240, 80, 140),
        make_stream(180, 150, 30)
    ]

    analyzer = StreamAnalyzer(default_temp_shift, streams)

    print(param_dict["title"])
    print(summary(analyzer))

    fig, ax = plot_results(analyzer, param_dict)
    plt.show()


def aromatics_plant():
    # Aromatics plant from
    # Pinch Analysis and Process Integration:
    # A User Guide On Process Integration for the Efficient Use of Energy,
    # Second edition, Ian C. Kemp, page 330
    param_dict = {
        "title": "Aromatics plant",
        "hcc_ccc_title": "Hot and cold composite curves",
        "hcc_ccc_xlabel": "Heat flow [ttc/h]",
        "hcc_ccc_ylabel": "Actual temperature [\u2103]",
        "gcc_title": "Grand composite curve",
        "gcc_xlabel": "Net heat flow [ttc/h]",
        "gcc_ylabel": "Shifted temperature [\u2103]",
        "hcc_style": HCC_STYLE,
        "ccc_style": CCC_STYLE,
        "gcc_style": GCC_STYLE,
    }

    min_temp_diff = 10
    default_temp_shift = min_temp_diff / 2

    # Some of the streams consist of multiple segments with individual heat
    # capacities
    streams = [
        make_segmented_stream([-13.9, 102, 229], [-8.3, 229, 327]),
        make_segmented_stream([13.9, 327, 174], [9, 174, 92], [4.2, 92, 50]),
        make_stream(-9, 35, 164),
        make_segmented_stream(
            [-7.2, 140, 176], [-25.2, 176, 367], [-16.4, 367, 500]),
        make_stream(25.2, 495, 307),
        make_segmented_stream(
            [7.2, 220, 160], [3.3, 160, 144], [4.1, 144, 125], [11.6, 125, 59]),
        make_stream(-3.3, 80, 123),
        make_stream(-6.8, 59, 169),
        make_segmented_stream([6.8, 220, 130], [3.8, 130, 67]),
        make_stream(-4.1, 85, 125),
        make_stream(-32.5, 480, 500)
    ]

    analyzer = StreamAnalyzer(default_temp_shift, streams)

    print(param_dict["title"])
    print(summary(analyzer))

    plot_results(analyzer, param_dict)
    plt.show()


def evaporator_dryer_plant():
    # Evaporator/dryer plant from
    # Pinch Analysis and Process Integration:
    # A User Guide On Process Integration for the Efficient Use of Energy,
    # Second edition, Ian C. Kemp, page 351
    param_dict = {
        "title": "Evaporator/dryer plant",
        "hcc_ccc_title": "Hot and cold composite curves",
        "hcc_ccc_xlabel": "Heat flow [kW]",
        "hcc_ccc_ylabel": "Actual temperature [\u2103]",
        "gcc_title": "Grand composite curve",
        "gcc_xlabel": "Net heat flow [kW]",
        "gcc_ylabel": "Shifted temperature [\u2103]",
        "hcc_style": HCC_STYLE,
        "ccc_style": CCC_STYLE,
        "gcc_style": GCC_STYLE,
    }

    min_temp_diff = 5.5
    default_temp_shift = min_temp_diff / 2

    # Some of the streams have equal supply and target temperatures, meaning
    # that they transfer latent heat
    evaporator_streams = [
        make_stream(-183, 10, 70),
        make_stream(-198, 37.8, 87.8),
        make_stream(-1005.5, 79.4, 79.4),
        make_stream(1039, 79.4, 79.4),
        make_stream(232, 86.9, 10),
        make_stream(-643, 48.8, 48.8),
        make_stream(714, 43.3, 43.3),
        make_segmented_stream([-6.5, 48.8, 54.4], [-263.5, 54.4, 93.3]),
        make_stream(260, 43.3, 43.3),
        make_stream(57, 43.3, 10)
    ]

    dryer_streams = [
        make_stream(-93.5, 55, 55),
        make_stream(-254, 41, 41),
        make_stream(-124, 60, 60),
        # Some optional streams
        # make_stream(149, 41, 13),
        # make_stream(140, 60, 13),
        # make_stream(189, 55, 13)
    ]

    analyzer = StreamAnalyzer(default_temp_shift)
    analyzer.add(evaporator_streams)
    analyzer.add(dryer_streams)

    print(param_dict["title"])
    print(summary(analyzer))

    fig, ax = plot_results(analyzer, param_dict)
    plt.show()


if __name__ == "__main__":
    four_stream()
    aromatics_plant()
    evaporator_dryer_plant()
