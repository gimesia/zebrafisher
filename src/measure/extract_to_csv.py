import os
from csv import reader, DictWriter
from datetime import datetime

from ..models import InputImage

header = [
    "Date",
    "Time",
    "Successful",
    "Name",
    "Has_Fish",
    "Major_Axis",
    "Minor_Axis",
    "Axes_ratio",
    "Has_Eyes",
    "Eye1_Diameter_major",
    "Eye2_Diameter_major",
    "Resolution",
    "Area",
    "Comment"
]

cwd = os.path.abspath("..")
path = os.path.join(cwd, "src", "images", "out")
files = os.listdir(path)
path = os.path.join(path, "results.csv")

if not files.__contains__("results.csv"):
    with open(path, "w", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)
        writer.writeheader()


def put_analysis_result_into_csv(input_img: InputImage) -> None:
    global header

    lines = get_csv_lines()

    if len(lines) == 0 or lines[0][0] != header[0]:
        print("Creating CSV")
        create_csv()

    # writerow_from_measurement(input_img.measurements, input_img.name)
    writerow_from_input_image(input_img)
    return


def get_csv_lines() -> list:
    """
    Extracts lines from the cvs file defined by the path

    :rtype: array of the lines
    """
    global path

    rows = []
    try:
        with open(path, 'r') as read_obj:
            csv_reader = reader(read_obj)
            for row in csv_reader:
                rows.append(row)
    except():
        pass
    return rows


def create_csv(head=None):
    global header
    global path

    if head is None:
        head = header

    with open(path, "a", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)
        writer.writeheader()


def writerow_empty():
    """
    Writes a row with a writer according to the given measurement object and name

    :param writer: csv.DictWriter object
    :param measurements: Measurements object
    :param name: Name of object
    """
    global header
    with open(path, "a", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)

        writer.writerow({
            "Date": "",
            "Time": "",
            "Successful": "",
            "Name": "",
            "Has_Fish": "",
            "Major_Axis": "",
            "Minor_Axis": "",
            "Axes_ratio": "",
            "Has_Eyes": "",
            "Eye1_Diameter_major": "",
            "Eye2_Diameter_major": "",
            "Resolution": "",
            "Area": "",
            "Comment": ""
        })


def writerow_from_input_image(input_img: InputImage):
    """
    Writes a row with a writer according to the given measurement object and name

    :param input_img:
    """
    global header
    measurements = input_img.measurements

    with open(path, "a", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)
        writer.writerow({
            "Date": str(datetime.now().date()),
            "Time": str(datetime.now().time()),
            "Name": input_img.name,
            "Successful": input_img.success,
            "Has_Fish": input_img.fish_props.has_fish,
            "Major_Axis": measurements.axis_major,
            "Minor_Axis": measurements.axis_minor,
            "Axes_ratio": measurements.axes_ratio,
            "Has_Eyes": measurements.eye_count,
            "Eye1_Diameter_major": measurements.eye1_diameter_major,
            "Eye2_Diameter_major": measurements.eye2_diameter_major,
            "Resolution": measurements.resolution,
            "Area": measurements.area,
            "Comment": ""
        })
