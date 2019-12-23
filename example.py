from matplotlib import pyplot as plt

from pinch import segments
from pinch.stream import Stream
from pinch.stream_group import StreamGroup


def four_stream():
    min_temp_diff = 10
    default_temp_diff_contrib = min_temp_diff / 2

    streams = []
    streams.append(Stream([segments.new(230, 20, 135)]))
    streams.append(Stream([segments.new(-330, 170, 60)]))
    streams.append(Stream([segments.new(240, 80, 140)]))
    streams.append(Stream([segments.new(-180, 150, 30)]))

    stream_group = StreamGroup(default_temp_diff_contrib, streams)

    print("Hot utility: {:0.2f}".format(stream_group.hot_utility_target))
    print("Cold utility: {:0.2f}".format(stream_group.cold_utility_target))

    cold_heat_flows, cold_temps = stream_group.cold_cascade.cumulative_heat_flow
    hot_heat_flows, hot_temps = stream_group.hot_cascade.cumulative_heat_flow
    plt.plot(cold_heat_flows, cold_temps)
    plt.plot(hot_heat_flows, hot_temps)
    plt.show()

    grand_heat_flows, grand_temps = \
        stream_group.shifted_grand_cascade.cumulative_heat_flow
    plt.plot(grand_heat_flows, grand_temps)
    plt.show()


def aromatics_plant():
    min_temp_diff = 10
    default_temp_diff_contrib = min_temp_diff / 2

    streams = []
    streams.append(Stream([
        segments.new(13.9, 102, 229),
        segments.new(8.3, 229, 327)
    ]))
    streams.append(Stream([
        segments.new(-13.9, 327, 174),
        segments.new(-9, 174, 92),
        segments.new(-4.2, 92, 50)
    ]))
    streams.append(Stream([segments.new(9, 35, 164)]))
    streams.append(Stream([
        segments.new(7.2, 140, 176),
        segments.new(25.2, 176, 367),
        segments.new(16.4, 367, 500)
    ]))
    streams.append(Stream([segments.new(-25.2, 495, 307)]))
    streams.append(Stream([
        segments.new(-7.2, 220, 160),
        segments.new(-3.3, 160, 144),
        segments.new(-4.1, 144, 125),
        segments.new(-11.6, 125, 59)
    ]))
    streams.append(Stream([segments.new(3.3, 80, 123)]))
    streams.append(Stream([segments.new(6.8, 59, 169)]))
    streams.append(Stream([
        segments.new(-6.8, 220, 130),
        segments.new(-3.8, 130, 67)
    ]))
    streams.append(Stream([segments.new(4.1, 85, 125)]))
    streams.append(Stream([segments.new(32.5, 480, 500)]))

    stream_group = StreamGroup(default_temp_diff_contrib, streams)

    print("Hot utility: {:0.2f}".format(stream_group.hot_utility_target))
    print("Cold utility: {:0.2f}".format(stream_group.cold_utility_target))

    cold_heat_flows, cold_temps = stream_group.cold_cascade.cumulative_heat_flow
    hot_heat_flows, hot_temps = stream_group.hot_cascade.cumulative_heat_flow
    plt.plot(cold_heat_flows, cold_temps)
    plt.plot(hot_heat_flows, hot_temps)
    plt.show()

    grand_heat_flows, grand_temps = \
        stream_group.shifted_grand_cascade.cumulative_heat_flow
    plt.plot(grand_heat_flows, grand_temps)
    plt.show()


if __name__ == "__main__":
    four_stream()
    aromatics_plant()
