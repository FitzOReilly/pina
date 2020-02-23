from matplotlib import pyplot as plt

from pinch import segment
from pinch.stream import Stream
from pinch.stream_group import StreamGroup


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
        Stream([segment.new(-230, 20, 135)]),
        Stream([segment.new(330, 170, 60)]),
        Stream([segment.new(-240, 80, 140)]),
        Stream([segment.new(180, 150, 30)])
    ]

    stream_group = StreamGroup(default_temp_shift, streams)

    print(
        "Heating demand: {0:0.2f}\n"
        "Cooling demand: {1:0.2f}\n"
        "Hot utility target: {2:0.2f}\n"
        "Cold utility target: {3:0.2f}\n"
        "Heat recovery target: {4:0.2f}\n"
        "Pinch temperature(s): {5}\n"
        .format(
            stream_group.heating_demand, stream_group.cooling_demand,
            stream_group.hot_utility_target, stream_group.cold_utility_target,
            stream_group.heat_recovery_target, stream_group.pinch_temps))

    fig, ax = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.suptitle("Four stream example", fontweight="bold")

    ax[0].plot(*stream_group.hot_cascade.cumulative_heat_flow, **HCC_STYLE)
    ax[0].plot(*stream_group.cold_cascade.cumulative_heat_flow, **CCC_STYLE)
    ax[0].legend()
    ax[0].set_title("Hot and cold composite curves")
    ax[0].set_xlabel("Heat flow [kW]")
    ax[0].set_ylabel("Actual temperature [\u2103]")

    ax[1].plot(*stream_group.grand_cascade.cumulative_heat_flow, **GCC_STYLE)
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
    streams.append(Stream([
        segment.new(-13.9, 102, 229),
        segment.new(-8.3, 229, 327)
    ]))
    streams.append(Stream([
        segment.new(13.9, 327, 174),
        segment.new(9, 174, 92),
        segment.new(4.2, 92, 50)
    ]))
    streams.append(Stream([segment.new(-9, 35, 164)]))
    streams.append(Stream([
        segment.new(-7.2, 140, 176),
        segment.new(-25.2, 176, 367),
        segment.new(-16.4, 367, 500)
    ]))
    streams.append(Stream([segment.new(25.2, 495, 307)]))
    streams.append(Stream([
        segment.new(7.2, 220, 160),
        segment.new(3.3, 160, 144),
        segment.new(4.1, 144, 125),
        segment.new(11.6, 125, 59)
    ]))
    streams.append(Stream([segment.new(-3.3, 80, 123)]))
    streams.append(Stream([segment.new(-6.8, 59, 169)]))
    streams.append(Stream([
        segment.new(6.8, 220, 130),
        segment.new(3.8, 130, 67)
    ]))
    streams.append(Stream([segment.new(-4.1, 85, 125)]))
    streams.append(Stream([segment.new(-32.5, 480, 500)]))

    stream_group = StreamGroup(default_temp_shift, streams)

    print(
        "Heating demand: {0:0.2f}\n"
        "Cooling demand: {1:0.2f}\n"
        "Hot utility target: {2:0.2f}\n"
        "Cold utility target: {3:0.2f}\n"
        "Heat recovery target: {4:0.2f}\n"
        "Pinch temperature(s): {5}\n"
        .format(
            stream_group.heating_demand, stream_group.cooling_demand,
            stream_group.hot_utility_target, stream_group.cold_utility_target,
            stream_group.heat_recovery_target, stream_group.pinch_temps))

    fig, ax = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.suptitle("Aromatics plant", fontweight="bold")

    ax[0].plot(*stream_group.hot_cascade.cumulative_heat_flow, **HCC_STYLE)
    ax[0].plot(*stream_group.cold_cascade.cumulative_heat_flow, **CCC_STYLE)
    ax[0].legend()
    ax[0].set_title("Hot and cold composite curves")
    ax[0].set_xlabel("Heat flow [ttc/h]")
    ax[0].set_ylabel("Actual temperature [\u2103]")

    ax[1].plot(*stream_group.grand_cascade.cumulative_heat_flow, **GCC_STYLE)
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
    evaporator_streams.append(Stream([segment.new(-183, 10, 70)]))
    evaporator_streams.append(Stream([segment.new(-198, 37.8, 87.8)]))
    # Stream segments can have equal supply and target temperatures
    # (which means they transfer latent heat)
    evaporator_streams.append(Stream([segment.new(-1005.5, 79.4, 79.4)]))
    evaporator_streams.append(Stream([segment.new(1039, 79.4, 79.4)]))
    evaporator_streams.append(Stream([segment.new(232, 86.9, 10)]))
    evaporator_streams.append(Stream([segment.new(-643, 48.8, 48.8)]))
    evaporator_streams.append(Stream([segment.new(714, 43.3, 43.3)]))
    evaporator_streams.append(Stream([
        segment.new(-6.5, 48.8, 54.4),
        segment.new(-263.5, 54.4, 93.3)
    ]))
    evaporator_streams.append(Stream([segment.new(260, 43.3, 43.3)]))
    evaporator_streams.append(Stream([segment.new(57, 43.3, 10)]))

    dryer_streams = []
    dryer_streams.append(Stream([segment.new(-93.5, 55, 55)]))
    dryer_streams.append(Stream([segment.new(-254, 41, 41)]))
    dryer_streams.append(Stream([segment.new(-124, 60, 60)]))
    # dryer_streams.append(Stream([segment.new(149, 41, 13)]))
    # dryer_streams.append(Stream([segment.new(140, 60, 13)]))
    # dryer_streams.append(Stream([segment.new(189, 55, 13)]))

    stream_group = StreamGroup(default_temp_shift)
    stream_group.add(evaporator_streams)
    stream_group.add(dryer_streams)

    print(
        "Heating demand: {0:0.2f}\n"
        "Cooling demand: {1:0.2f}\n"
        "Hot utility target: {2:0.2f}\n"
        "Cold utility target: {3:0.2f}\n"
        "Heat recovery target: {4:0.2f}\n"
        "Pinch temperature(s): {5}\n"
        .format(
            stream_group.heating_demand, stream_group.cooling_demand,
            stream_group.hot_utility_target, stream_group.cold_utility_target,
            stream_group.heat_recovery_target, stream_group.pinch_temps))

    fig, ax = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.suptitle("Evaporator/dryer plant", fontweight="bold")

    ax[0].plot(*stream_group.hot_cascade.cumulative_heat_flow, **HCC_STYLE)
    ax[0].plot(*stream_group.cold_cascade.cumulative_heat_flow, **CCC_STYLE)
    ax[0].legend()
    ax[0].set_title("Hot and cold composite curves")
    ax[0].set_xlabel("Heat flow [kW]")
    ax[0].set_ylabel("Actual temperature [\u2103]")

    ax[1].plot(*stream_group.grand_cascade.cumulative_heat_flow, **GCC_STYLE)
    ax[1].legend()
    ax[1].set_title("Grand composite curve")
    ax[1].set_xlabel("Net heat flow [kW]")
    ax[1].set_ylabel("Shifted temperature [\u2103]")
    ax[1].set_ylim(ax[0].get_ylim())

    plt.show()


if __name__ == "__main__":
    four_stream()
    aromatics_plant()
    evaporator_dryer_plant()
