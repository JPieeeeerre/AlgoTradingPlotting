import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class AlgoTradingPlotting ():

    def plotForex(data, window, dpi, size, points=None, channels=None, lines=None, number_candles=3000):

        start = 0
        up_color = "Green"
        down_color = "Red"

        scope = len(data)-number_candles

        # Slices the data:
        data_original = data
        points_original = points
        channels_original = channels
        lines_original = lines

        data = data[scope:]
        data = data.reset_index(drop=True)


        if channels is not None:
            channels = channels[-number_candles:]
            channels = channels.reset_index(drop=True)
        if points is not None:
            points = points[points["X"] > scope]
            points = points.reset_index(drop=True)
            points["X"] = points["X"] - scope
        if lines is not None:
            lines = lines[-number_candles:]
            lines = lines.reset_index(drop=True)


        for end in range(start, len(data), window):
            if end > 0:

                plt.figure(figsize=size, dpi=dpi)

                # Slices the data into a window:
                data_2 = data[start:end]

                if points is not None:
                    points_bigger = points.loc[points["X"] > start]
                    points_in_window = points_bigger.loc[points_bigger["X"] < end]

                if channels is not None:
                    channels_greater_start = channels.loc[channels["X2"]>start]
                    channels_in_window = channels_greater_start.loc[channels_greater_start["X1"] < end]
                if lines is not None:
                    lines_greater_start = lines.loc[lines["X"]>start]
                    lines_in_window = lines_greater_start.loc[lines_greater_start["X"]<end]


                # Gets the up and down candles:
                up = data_2.loc[data_2.Close >= data_2.Open]
                down = data_2.loc[data_2.Close <= data_2.Open]

                # plot up prices
                plt.bar(up.index, up.Close - up.Open, 0.8, bottom=up.Open, color=up_color)
                plt.bar(up.index, up.High - up.Close, 0.2, bottom=up.Close, color=up_color)
                plt.bar(up.index, up.Low - up.Open, 0.2, bottom=up.Open, color=up_color)

                # plot down prices
                plt.bar(down.index, down.Close - down.Open, 0.8, bottom=down.Open, color=down_color)
                plt.bar(down.index, down.High - down.Open, 0.2, bottom=down.Open, color=down_color)
                plt.bar(down.index, down.Low - down.Close, 0.2, bottom=down.Close, color=down_color)

                # Plots points:
                if points is not None:
                    for point_index in points_in_window.index:
                        plt.plot(points_in_window["X"][point_index],points_in_window["Y"][point_index],".", color=points_in_window["Color"][point_index], zorder=-10)

                # Plots channels:
                if channels is not None:
                    if channels_in_window is not None:

                        for c_ind in channels_in_window.index:

                            # If channel X1 is greater than start:
                            if channels_in_window["X1"][c_ind] >= start:

                                # If channel X2 is less than end:
                                if channels_in_window["X2"][c_ind] <= end:
                                    plt.plot([channels_in_window["X1"][c_ind],channels_in_window["X2"][c_ind]], [channels_in_window["Y1"][c_ind],channels_in_window["Y1"][c_ind]], color=channels_in_window["Color"][c_ind],linewidth = 0.4, zorder =-5)
                                    plt.plot([channels_in_window["X1"][c_ind], channels_in_window["X2"][c_ind]],
                                             [channels_in_window["Y2"][c_ind], channels_in_window["Y2"][c_ind]],
                                             color=channels_in_window["Color"][c_ind],linewidth = 0.4, zorder=-5)
                                else:
                                    plt.plot([channels_in_window["X1"][c_ind], end],
                                             [channels_in_window["Y1"][c_ind], channels_in_window["Y1"][c_ind]],
                                             color=channels_in_window["Color"][c_ind],linewidth = 0.4, zorder=-5)
                                    plt.plot([channels_in_window["X1"][c_ind], end],
                                             [channels_in_window["Y2"][c_ind], channels_in_window["Y2"][c_ind]],
                                             color=channels_in_window["Color"][c_ind],linewidth = 0.4, zorder=-5)
                            else:
                                # If channel X2 is less than end:
                                if channels_in_window["X2"][c_ind] <= end:
                                    plt.plot([start, channels_in_window["X2"][c_ind]],
                                             [channels_in_window["Y1"][c_ind], channels_in_window["Y1"][c_ind]],
                                             color=channels_in_window["Color"][c_ind],linewidth = 0.4, zorder=-5)
                                    plt.plot([start, channels_in_window["X2"][c_ind]],
                                             [channels_in_window["Y2"][c_ind], channels_in_window["Y2"][c_ind]],
                                             color=channels_in_window["Color"][c_ind],linewidth = 0.4, zorder=-5)
                                else:
                                    plt.plot([start, end],
                                             [channels_in_window["Y1"][c_ind], channels_in_window["Y1"][c_ind]],
                                             color=channels_in_window["Color"][c_ind],linewidth = 0.4, zorder=-5)
                                    plt.plot([start, end],
                                             [channels_in_window["Y2"][c_ind], channels_in_window["Y2"][c_ind]],
                                             color=channels_in_window["Color"][c_ind], linewidth = 0.4, zorder=-5)


                # Plots lines:
                if lines is not None:
                    plt.plot(lines_in_window["X"], lines_in_window["Y"], color=lines_in_window["Color"], zorder=-8)

                start = start + window

