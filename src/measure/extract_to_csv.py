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
    "Eye1_Diameter",
    "Eye2_Diameter",
    "Resolution",
    "Area",
    "Comment"
]

cwd = os.path.abspath("..")
path = os.path.join(cwd, "src", "images")
files = os.listdir(path)
path_t = os.path.join(path, "result_times.csv")
path = os.path.join(path, "results.csv")

if not files.__contains__("results.csv"):
    with open(path, "w", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)
        writer.writeheader()


def measurements_to_csv(input_img: InputImage) -> None:
    """
    Extracts the measurement values into the csv file defined in 'path'

    :param input_img: input object with measurements
    :return: None
    """
    global header

    lines = get_csv_lines()

    if len(lines) == 0 or lines[0][0] != header[0]:
        print("Creating CSV")
        create_result_csv()

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


def create_result_csv() -> None:
    """
    Creates csv for results
    TODO examine if really needed (it autocreates if it cannot find the given name)
    """
    global header
    global path

    with open(path, "a", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)
        writer.writeheader()


def writerow_empty(name=""):
    """
    Writes a row with a writer according to the given measurement object and name

    :param name: Name of object
    """
    global header
    with open(path, "a", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)

        writer.writerow({
            "Date": "",
            "Time": "",
            "Successful": "",
            "Name": name,
            "Has_Fish": "",
            "Major_Axis": "",
            "Minor_Axis": "",
            "Axes_ratio": "",
            "Has_Eyes": "",
            "Eye1_Diameter": "",
            "Eye2_Diameter": "",
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
            "Eye1_Diameter": measurements.eye1_diameter_major,
            "Eye2_Diameter": measurements.eye2_diameter_major,
            "Resolution": measurements.resolution,
            "Area": measurements.area,
            "Comment": ""
        })


def measurement_times_csv(inp: list[str]):
    """
    Extracts runtimes into destination
    :param inp:
    """
    h = ["batch_name", "name", "well_loc", "fish_loc", "measure", "start2end"]
    with open(path_t, "a", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=h)

        writer.writerow({
            h[0]: inp[0],
            h[1]: inp[1],
            h[2]: inp[2],
            h[3]: inp[3],
            h[4]: inp[4],
            h[5]: inp[5]
        })
