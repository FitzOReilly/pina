from matplotlib import pyplot as plt

from pina import PinchAnalyzer, make_segmented_stream, make_stream

# Some customizations to make the plots pretty
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
PLOT_PARAMS = {
    "title": "",
    "hcc_ccc_title": "Hot and cold composite curves",
    "hcc_ccc_xlabel": "Heat flow [kW]",
    "hcc_ccc_ylabel": "Actual temperature [\u2103]",
    "gcc_title": "Grand composite curve",
    "gcc_xlabel": "Net heat flow [kW]",
    "gcc_ylabel": "Shifted temperature [\u2103]",
    "figsize": (16, 7),
    "hcc_style": HCC_STYLE,
    "ccc_style": CCC_STYLE,
    "gcc_style": GCC_STYLE,
}


def describe(pinch_analyzer):
    """
    Returns a string with the energy targets and the pinch temperature(s).
    """
    names = [
        "Heating demand:",
        "Cooling demand:",
        "Hot utility target:",
        "Cold utility target:",
        "Heat recovery target:",
        "Pinch temperature(s):",
    ]
    values = [
        pinch_analyzer.heating_demand,
        pinch_analyzer.cooling_demand,
        pinch_analyzer.hot_utility_target,
        pinch_analyzer.cold_utility_target,
        pinch_analyzer.heat_recovery_target,
        pinch_analyzer.pinch_temps,
    ]
    max_width = max(len(n) for n in names)
    return "".join(
        "{:{width}} {}\n".format(n, v, width=max_width) for n, v in zip(names, values)
    )


def plot_results(pinch_analyzer, param_dict):
    """
    Creates two plots: One of the hot and cold composite curves and one of the
    grand composite curve. Returns a tuple with the figure and axes objects.
    """
    fig, ax = plt.subplots(1, 2, figsize=param_dict["figsize"])
    fig.suptitle(param_dict["title"], fontweight="bold")

    ax[0].plot(*pinch_analyzer.hot_composite_curve, **param_dict["hcc_style"])
    ax[0].plot(*pinch_analyzer.cold_composite_curve, **param_dict["ccc_style"])
    ax[0].legend()
    ax[0].set_title(param_dict["hcc_ccc_title"])
    ax[0].set_xlabel(param_dict["hcc_ccc_xlabel"])
    ax[0].set_ylabel(param_dict["hcc_ccc_ylabel"])

    ax[1].plot(*pinch_analyzer.grand_composite_curve, **param_dict["gcc_style"])
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
    param_dict = dict(PLOT_PARAMS)
    param_dict["title"] = "Four stream example"

    min_temp_diff = 10
    default_temp_shift = min_temp_diff / 2

    streams = [
        make_stream(-230, 20, 135),
        make_stream(330, 170, 60),
        make_stream(-240, 80, 140),
        make_stream(180, 150, 30),
    ]

    analyzer = PinchAnalyzer(default_temp_shift)
    analyzer.add_streams(*streams)

    print(param_dict["title"])
    print(describe(analyzer))

    fig, ax = plot_results(analyzer, param_dict)
    plt.show()


def aromatics_plant():
    # Aromatics plant from
    # Pinch Analysis and Process Integration:
    # A User Guide On Process Integration for the Efficient Use of Energy,
    # Second edition, Ian C. Kemp, page 330
    param_dict = dict(PLOT_PARAMS)
    param_dict.update(
        {
            "title": "Aromatics plant",
            "hcc_ccc_xlabel": "Heat flow [ttc/h]",
            "gcc_xlabel": "Net heat flow [ttc/h]",
        }
    )

    min_temp_diff = 10
    default_temp_shift = min_temp_diff / 2

    # Some of the streams consist of multiple segments with individual heat
    # capacities
    streams = [
        make_segmented_stream([-13.9, 102, 229], [-8.3, 229, 327]),
        make_segmented_stream([13.9, 327, 174], [9, 174, 92], [4.2, 92, 50]),
        make_stream(-9, 35, 164),
        make_segmented_stream([-7.2, 140, 176], [-25.2, 176, 367], [-16.4, 367, 500]),
        make_stream(25.2, 495, 307),
        make_segmented_stream(
            [7.2, 220, 160], [3.3, 160, 144], [4.1, 144, 125], [11.6, 125, 59]
        ),
        make_stream(-3.3, 80, 123),
        make_stream(-6.8, 59, 169),
        make_segmented_stream([6.8, 220, 130], [3.8, 130, 67]),
        make_stream(-4.1, 85, 125),
        make_stream(-32.5, 480, 500),
    ]

    analyzer = PinchAnalyzer(default_temp_shift)
    analyzer.add_streams(*streams)

    print(param_dict["title"])
    print(describe(analyzer))

    plot_results(analyzer, param_dict)
    plt.show()


def evaporator_dryer_plant():
    # Evaporator/dryer plant from
    # Pinch Analysis and Process Integration:
    # A User Guide On Process Integration for the Efficient Use of Energy,
    # Second edition, Ian C. Kemp, page 351
    param_dict = dict(PLOT_PARAMS)
    param_dict["title"] = "Evaporator/dryer plant"

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
        make_stream(57, 43.3, 10),
    ]

    dryer_streams = [
        make_stream(-93.5, 55, 55),
        make_stream(-254, 41, 41),
        make_stream(-124, 60, 60),
        # Some optional streams
        # make_stream(149, 41, 13),
        # make_stream(140, 60, 13),
        # make_stream(189, 55, 13),
    ]

    analyzer = PinchAnalyzer(default_temp_shift)
    analyzer.add_streams(*evaporator_streams)
    analyzer.add_streams(*dryer_streams)

    print(param_dict["title"])
    print(describe(analyzer))

    fig, ax = plot_results(analyzer, param_dict)
    plt.show()


def multiple_pinches():
    # A made-up example with multiple pinches
    param_dict = dict(PLOT_PARAMS)
    param_dict["title"] = "Multiple pinches"

    min_temp_diff = 10
    default_temp_shift = min_temp_diff / 2

    cold_1 = make_stream(-360, 30, 150)
    hot_1 = make_segmented_stream(
        [20, 140, 100],
        [90, 100, 100],  # A latent segment to model condensation
        [30, 100, 60],
    )
    # The PinchAnalyzer's default temp_shift will be ignored for this stream.
    cold_2 = make_stream(-20, 5, 20, temp_shift=2)
    hot_2 = make_stream(160, 60, 20)

    analyzer = PinchAnalyzer(default_temp_shift)
    analyzer.add_streams(cold_1, hot_1, cold_2, hot_2)

    print(param_dict["title"])
    print(describe(analyzer))

    fig, ax = plot_results(analyzer, param_dict)
    plt.show()


def banana():
    param_dict = dict(PLOT_PARAMS)
    param_dict["title"] = "Banana"

    min_temp_diff = 5
    default_temp_shift = min_temp_diff / 2

    cold = make_segmented_stream(
        [-4, 10, 10],
        [-4, 10, 10.25],
        [-3, 10.25, 10.5],
        [-4, 10.5, 11],
        [-5, 11, 12],
        [-10, 12, 15],
        [-10, 15, 18],
        [-5, 18, 20],
        [-5, 20, 22],
        [-4.5, 22, 24],
        [-6, 24, 28],
        [-5.5, 28, 34],
        [-3, 34, 39],
        [-4, 39, 48],
        [-0.5, 48, 49.5],
        [-0.5, 49.5, 52],
        [-0.5, 52, 55],
        [0, 55, 61],
        [-0.5, 61, 65.5],
        [-0.5, 65.5, 67],
        [-2, 67, 70],
        [-1, 70, 71],
        [-1.5, 71, 72],
    )

    hot = make_segmented_stream(
        [1, 74, 71],
        [1, 71, 68.5],
        [1, 68.5, 67],
        [1, 67, 65.5],
        [1, 65.5, 64.5],
        [1, 64.5, 63.5],
        [2.5, 63.5, 63],
        [2.5, 63, 62],
        [2.5, 62, 60],
        [1.5, 60, 58.5],
        [1, 58.5, 57],
        [5, 57, 50],
        [5, 50, 45],
        [5, 45, 41],
        [5, 41, 38],
        [5, 38, 36],
        [5, 36, 34],
        [5, 34, 32],
        [5, 32, 30],
        [5, 30, 28],
        [6, 28, 25],
        [5, 25, 21],
        [4, 21, 17],
    )

    analyzer = PinchAnalyzer(default_temp_shift)
    analyzer.add_streams(cold, hot)

    print(param_dict["title"])
    print(describe(analyzer))

    fig, ax = plot_results(analyzer, param_dict)
    plt.show()


if __name__ == "__main__":
    four_stream()
    aromatics_plant()
    evaporator_dryer_plant()
    multiple_pinches()
    banana()
