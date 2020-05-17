from matplotlib import pyplot as plt

from pinch import stream
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


def four_stream():
    # Four stream example from
    # Pinch Analysis and Process Integration:
    # A User Guide On Process Integration for the Efficient Use of Energy,
    # Second edition, Ian C. Kemp, page 4
    print("Four stream example")
    min_temp_diff = 10
    default_temp_shift = min_temp_diff / 2

    streams = [
        stream.new(-230, 20, 135),
        stream.new(330, 170, 60),
        stream.new(-240, 80, 140),
        stream.new(180, 150, 30)
    ]

    analyzer = StreamAnalyzer(default_temp_shift, streams)

    print(
        "Heating demand: {0:0.2f}\n"
        "Cooling demand: {1:0.2f}\n"
        "Hot utility target: {2:0.2f}\n"
        "Cold utility target: {3:0.2f}\n"
        "Heat recovery target: {4:0.2f}\n"
        "Pinch temperature(s): {5}\n"
        .format(
            analyzer.heating_demand, analyzer.cooling_demand,
            analyzer.hot_utility_target, analyzer.cold_utility_target,
            analyzer.heat_recovery_target, analyzer.pinch_temps))

    fig, ax = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.suptitle("Four stream example", fontweight="bold")

    ax[0].plot(*analyzer.hot_composite_curve, **HCC_STYLE)
    ax[0].plot(*analyzer.cold_composite_curve, **CCC_STYLE)
    ax[0].legend()
    ax[0].set_title("Hot and cold composite curves")
    ax[0].set_xlabel("Heat flow [kW]")
    ax[0].set_ylabel("Actual temperature [\u2103]")

    ax[1].plot(*analyzer.grand_composite_curve, **GCC_STYLE)
    ax[1].legend()
    ax[1].set_title("Grand composite curve")
    ax[1].set_xlabel("Net heat flow [kW]")
    ax[1].set_ylabel("Shifted temperature [\u2103]")
    ax[1].set_ylim(ax[0].get_ylim())

    plt.show()


def aromatics_plant():
    # Aromatics plant from
    # Pinch Analysis and Process Integration:
    # A User Guide On Process Integration for the Efficient Use of Energy,
    # Second edition, Ian C. Kemp, page 330
    print("Aromatics plant")
    min_temp_diff = 10
    default_temp_shift = min_temp_diff / 2

    streams = []
    # Streams can consist of multiple segments
    streams.append(stream.new_segmented(
        [-13.9, 102, 229],
        [-8.3, 229, 327]
    ))
    streams.append(stream.new_segmented(
        [13.9, 327, 174],
        [9, 174, 92],
        [4.2, 92, 50]
    ))
    streams.append(stream.new(-9, 35, 164))
    streams.append(stream.new_segmented(
        [-7.2, 140, 176],
        [-25.2, 176, 367],
        [-16.4, 367, 500]
    ))
    streams.append(stream.new(25.2, 495, 307))
    streams.append(stream.new_segmented(
        [7.2, 220, 160],
        [3.3, 160, 144],
        [4.1, 144, 125],
        [11.6, 125, 59]
    ))
    streams.append(stream.new(-3.3, 80, 123))
    streams.append(stream.new(-6.8, 59, 169))
    streams.append(stream.new_segmented(
        [6.8, 220, 130],
        [3.8, 130, 67]
    ))
    streams.append(stream.new(-4.1, 85, 125))
    streams.append(stream.new(-32.5, 480, 500))

    analyzer = StreamAnalyzer(default_temp_shift, streams)

    print(
        "Heating demand: {0:0.2f}\n"
        "Cooling demand: {1:0.2f}\n"
        "Hot utility target: {2:0.2f}\n"
        "Cold utility target: {3:0.2f}\n"
        "Heat recovery target: {4:0.2f}\n"
        "Pinch temperature(s): {5}\n"
        .format(
            analyzer.heating_demand, analyzer.cooling_demand,
            analyzer.hot_utility_target, analyzer.cold_utility_target,
            analyzer.heat_recovery_target, analyzer.pinch_temps))

    fig, ax = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.suptitle("Aromatics plant", fontweight="bold")

    ax[0].plot(*analyzer.hot_composite_curve, **HCC_STYLE)
    ax[0].plot(*analyzer.cold_composite_curve, **CCC_STYLE)
    ax[0].legend()
    ax[0].set_title("Hot and cold composite curves")
    ax[0].set_xlabel("Heat flow [ttc/h]")
    ax[0].set_ylabel("Actual temperature [\u2103]")

    ax[1].plot(*analyzer.grand_composite_curve, **GCC_STYLE)
    ax[1].legend()
    ax[1].set_title("Grand composite curve")
    ax[1].set_xlabel("Net heat flow [ttc/h]")
    ax[1].set_ylabel("Shifted temperature [\u2103]")
    ax[1].set_ylim(ax[0].get_ylim())

    plt.show()


def evaporator_dryer_plant():
    # Evaporator/dryer plant from
    # Pinch Analysis and Process Integration:
    # A User Guide On Process Integration for the Efficient Use of Energy,
    # Second edition, Ian C. Kemp, page 351
    print("Evaporator/dryer plant")
    min_temp_diff = 5.5
    default_temp_shift = min_temp_diff / 2

    evaporator_streams = []
    evaporator_streams.append(stream.new(-183, 10, 70))
    evaporator_streams.append(stream.new(-198, 37.8, 87.8))
    # Stream segments can have equal supply and target temperatures
    # (which means they transfer latent heat)
    evaporator_streams.append(stream.new(-1005.5, 79.4, 79.4))
    evaporator_streams.append(stream.new(1039, 79.4, 79.4))
    evaporator_streams.append(stream.new(232, 86.9, 10))
    evaporator_streams.append(stream.new(-643, 48.8, 48.8))
    evaporator_streams.append(stream.new(714, 43.3, 43.3))
    evaporator_streams.append(stream.new_segmented(
        [-6.5, 48.8, 54.4],
        [-263.5, 54.4, 93.3]
    ))
    evaporator_streams.append(stream.new(260, 43.3, 43.3))
    evaporator_streams.append(stream.new(57, 43.3, 10))

    dryer_streams = []
    dryer_streams.append(stream.new(-93.5, 55, 55))
    dryer_streams.append(stream.new(-254, 41, 41))
    dryer_streams.append(stream.new(-124, 60, 60))
    # dryer_streams.append(stream.new(149, 41, 13))
    # dryer_streams.append(stream.new(140, 60, 13))
    # dryer_streams.append(stream.new(189, 55, 13))

    analyzer = StreamAnalyzer(default_temp_shift)
    analyzer.add(evaporator_streams)
    analyzer.add(dryer_streams)

    print(
        "Heating demand: {0:0.2f}\n"
        "Cooling demand: {1:0.2f}\n"
        "Hot utility target: {2:0.2f}\n"
        "Cold utility target: {3:0.2f}\n"
        "Heat recovery target: {4:0.2f}\n"
        "Pinch temperature(s): {5}\n"
        .format(
            analyzer.heating_demand, analyzer.cooling_demand,
            analyzer.hot_utility_target, analyzer.cold_utility_target,
            analyzer.heat_recovery_target, analyzer.pinch_temps))

    fig, ax = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.suptitle("Evaporator/dryer plant", fontweight="bold")

    ax[0].plot(*analyzer.hot_composite_curve, **HCC_STYLE)
    ax[0].plot(*analyzer.cold_composite_curve, **CCC_STYLE)
    ax[0].legend()
    ax[0].set_title("Hot and cold composite curves")
    ax[0].set_xlabel("Heat flow [kW]")
    ax[0].set_ylabel("Actual temperature [\u2103]")

    # analyzer.grand_cascade.heat_offset = -200
    # analyzer.grand_cascade.add([segment.new(-1000, 0, 500)])
    ax[1].plot(*analyzer.grand_composite_curve, **GCC_STYLE)
    ax[1].legend()
    ax[1].set_title("Grand composite curve")
    ax[1].set_xlabel("Net heat flow [kW]")
    ax[1].set_ylabel("Shifted temperature [\u2103]")

    ylims = (*ax[0].get_ylim(), *ax[1].get_ylim())
    minmax_ylims = (min(ylims), max(ylims))
    ax[0].set_ylim(minmax_ylims)
    ax[1].set_ylim(minmax_ylims)

    plt.show()


if __name__ == "__main__":
    four_stream()
    aromatics_plant()
    evaporator_dryer_plant()
