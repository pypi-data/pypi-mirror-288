import os

import numpy as np
import pandas as pd


def extract_data(path):
    # Output
    data = []

    # Get file extension
    _, extension = os.path.splitext(path)

    # Extract file
    if extension == '.xlsx':
        data = pd.read_excel(path, skiprows=1)
    if extension == '.csv':
        data = pd.read_csv(path, skiprows=1)  # skiprows=1; To skip debris row in the dlc results
    return data


def read_bodyparts(data):
    # Parameters
    # data [DataFrame]: Return of 'extract_data'.
    # Return
    # bodyparts [list]: Name of bodyparts in the data.

    # Read data head
    head = data.head()

    # Read columns containing bodyparts
    bodyparts = list(head.columns[1:])  # 'bodyparts' in index=0

    return bodyparts


def extract_coordinates(data, x_bodypart, y_bodypart):
    # Parameters
    # data [DataFrame]: Return of 'extract_data'.
    # x_bodypart, y_bodypart [str]: Bodypart name to extract coordinates.
    # Return
    # x_coordinates, y_coordinates [list]: Coordinates for each bodypart.

    # Return
    x_coordinates, y_coordinates = [], []

    # Extract coordinates from each bodypart
    x_coordinates, y_coordinates = (list(map(float, data[x_bodypart][1:])),
                                    list(map(float, data[y_bodypart][1:])))

    return x_coordinates, y_coordinates


def make_route(x_coordinates, y_coordinates):
    return np.array([x_coordinates, y_coordinates])
