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
    "Head_Coords",
    "Tail_Coords",
    "Spine_Length",
    "Has_Eyes",
    "Eye1_Diameter_major",
    "Eye2_Diameter_major",
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
            "Date": str(datetime.now().date()),
            "Time": str(datetime.now().time()),
            "Name": "",
            "Successful": "",
            "Has_Fish": "",
            "Head_Coords": "",
            "Tail_Coords": "",
            "Spine_Length": "",
            "Has_Eyes": "",
            "Eye1_Diameter_major": "",
            "Eye2_Diameter_major": "",
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
            "Head_Coords": measurements.head_endpoint,
            "Tail_Coords": measurements.tail_endpoint,
            "Spine_Length": measurements.head_to_tail_length,
            "Has_Eyes": input_img.fish_props.has_eyes,
            "Eye1_Diameter_major": measurements.eye1_diameter_major,
            "Eye2_Diameter_major": measurements.eye2_diameter_major,
            "Area": False,
            "Comment": ""
        })
