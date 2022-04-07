from email import header
from fileinput import filename
import math
from CompAero import IsentropecRelations as irr
from bokeh.layouts import column, row
from bokeh.models.annotations import Legend
from bokeh.plotting import figure, show, output_file
import numpy as np
import pandas as pd


class Headers:
    staticPressure = "staticPressure"
    dynamicPressure = "dynamicPressure"
    accelX = "accelX"
    accelY = "accelY"
    accelZ = "accelZ"
    gyroX = "gyroX"
    gyroY = "gyroY"
    gyroZ = "gyroZ"

    columns = [
        staticPressure,
        dynamicPressure,
        accelX,
        accelY,
        accelZ,
        gyroX,
        gyroY,
        gyroZ,
    ]


FILE_NAME = "./crw_payload.data_samson_2_launch.csv"
HDR = Headers


def readFile() -> pd.DataFrame:
    # return pd.read_csv(FILE_NAME, usecols=HDR.columns, header=None)
    return pd.read_csv(FILE_NAME, header=None, names=HDR.columns,)


if __name__ == "__main__":
    df = readFile()

    pressRatio = df[HDR.staticPressure] / df[HDR.dynamicPressure]

    # Plots
    pressFig = figure(title="Pressure Data", plot_height=300, x_axis_label="Sample #", y_axis_label="Pressure PSI")
    pressRatioFig = figure(title="Pressure Data", plot_height=300, x_axis_label="Sample #", y_axis_label="Po/P")
    accelFig = figure(title="Accelerometer Data", plot_height=300, x_axis_label="Sample #", y_axis_label="Acceleration m/s^2")
    gyroDpsFig = figure(title="Gyro Data", plot_height=300, x_axis_label="Sample #", y_axis_label="Rotation Speed dps")
    gyroRpmFig = figure(title="Gyro Data", plot_height=300, x_axis_label="Sample #", y_axis_label="Rotation Speed RPM")
    velocityGraph = figure(title="Velocity From Pressure", plot_height=300, x_axis_label="Sample #", y_axis_label="Velocity ft/s")
    altitudeGraph = figure(title="Altitude From Static Pressure", plot_height=300, x_axis_label="Sample #", y_axis_label="Altitude ft")

    pressFig.line(x=df.index, y=df[HDR.staticPressure], color="blue", legend_label="Static Pressure")
    pressFig.line(x=df.index, y=df[HDR.dynamicPressure], color="red", legend_label="Dynamic Pressure")
    pressFig.legend.click_policy = "hide"

    pressRatioFig.line(x=df.index, y=pressRatio)

    accelFig.line(x=df.index, y=df[HDR.accelX], color="red", legend_label="X")
    accelFig.line(x=df.index, y=df[HDR.accelY], color="blue", legend_label="Y")
    accelFig.line(x=df.index, y=df[HDR.accelZ], color="green", legend_label="Z")
    accelFig.legend.click_policy = "hide"

    gyroDpsFig.line(x=df.index, y=df[HDR.gyroX], color="red", legend_label="X")
    gyroDpsFig.line(x=df.index, y=df[HDR.gyroY], color="blue", legend_label="Y")
    gyroDpsFig.line(x=df.index, y=df[HDR.gyroZ], color="green", legend_label="Z")
    gyroDpsFig.legend.click_policy = "hide"

    gyroRpmFig.line(x=df.index, y=df[HDR.gyroX] * 0.16666666666667, color="red", legend_label="X")
    gyroRpmFig.line(x=df.index, y=df[HDR.gyroY] * 0.16666666666667, color="blue", legend_label="Y")
    gyroRpmFig.line(x=df.index, y=df[HDR.gyroZ] * 0.16666666666667, color="green", legend_label="Z")
    gyroRpmFig.legend.click_policy = "hide"

    vels = math.sqrt(1.4 * 1716 * 529) * np.sqrt((np.power(pressRatio, (1.4 - 1) / 1.4) - 1) * 2 / (1.4 - 1))
    velocityGraph.line(x=df.index, y=vels, color="blue", legend_label="Pitot Probe")

    dp = (df[HDR.staticPressure] - 14.69) * 144  # psf
    alt = -dp / 0.0765

    altitudeGraph.line(df.index, alt)

    vel2 = np.diff(alt)
    vel2 = np.append(vel2, vel2[-1]) / 0.1

    # velocityGraph.line(x=df.index, y=vel2, color="red", legend_label="From Alt")
    velocityGraph.legend.click_policy = "hide"

    show(column(pressFig, pressRatioFig, velocityGraph, altitudeGraph, accelFig, gyroDpsFig, gyroRpmFig, sizing_mode="stretch_width"))

