import csv
from datetime import datetime
import os

import numpy as np

from ..models import InputImage, Measurements

cwd = os.path.abspath("..")
path = os.path.join(cwd, 'src', 'images', 'out', 'result.csv')
header = [
    "Date",
    "Time",
    "Successful",
    "Name",
    "Has_Fish",
    "Head_Coords",
    "Tail_Coords",
    "Spine_Length",
    "Has_Eyes",
    "Eye1_Diameter_major",
    "Eye2_Diameter_major",
    "Area"
]


def put_analysis_result_into_csv(input_img: InputImage) -> None:
    global header

    try:
        lines = get_csv_lines()
    except():
        lines = []

    if len(lines) == 0 or lines[0][0] != header[0]:
        print("Creating CSV")
        create_csv()

    # writerow_from_measurement(input_img.measurements, input_img.name)
    writerow_from_inputimage(input_img)
    return


def get_csv_lines() -> np.ndarray:
    """
    Extracts lines from the cvs file defined by the path

    :rtype: array of the lines
    """
    global path
    rows = np.genfromtxt(path, delimiter=',', dtype=str)
    return rows


def create_csv(head=None):
    global header
    global path

    if head is None:
        head = header

    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=head)
        writer.writeheader()


def writerow_from_array(measurements: list):
    """
    Writes a row with a writer according to the given measurement object and name

    :param writer: csv.DictWriter object
    :param measurements: Measurements object
    :param name: Name of object
    """
    global header
    with open(path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if len(measurements) < len(header):
            for i in range(len(measurements), len(header)):
                measurements.append('')
        writer.writerow({
            "Date": str(datetime.now().date()),
            "Time": str(datetime.now().time()),
            "Name": measurements[0],
            "Successful": measurements[0],
            "Has_Fish": 0,
            "Head_Coords": measurements[1],
            "Tail_Coords": measurements[2],
            "Spine_Length": measurements[3],
            "Has_Eyes": 0,
            "Eye1_Diameter_major": measurements[4],
            "Eye2_Diameter_major": measurements[5],
        })


def writerow_from_inputimage(input_img: InputImage):
    """
    Writes a row with a writer according to the given measurement object and name

    :param input_img:
    """
    global header
    measurements = input_img.measurements

    with open(path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writerow({
            "Date": str(datetime.now().date()),
            "Time": str(datetime.now().time()),
            "Name": input_img.name,
            "Successful": input_img.success,
            "Has_Fish": input_img.fish_props.has_fish,
            "Head_Coords": measurements.head_endpoint,
            "Tail_Coords": measurements.tail_endpoint,
            "Spine_Length": measurements.head_to_tail_length,
            "Has_Eyes": input_img.fish_props.has_eyes,
            "Eye1_Diameter_major": measurements.eye1_diameter_major,
            "Eye2_Diameter_major": measurements.eye2_diameter_major,
        })


if __name__ == '__main__':
    put_analysis_result_into_csv()
    print('fin')
