# Some links
# https://towardsdatascience.com/3d-data-processing-with-open3d-c3062aadc72e
# https://sketchfab.com/3Djimmetry/models visual reference for all artefacts

import csv
import logging.config
import pathlib
import sys
from typing import Iterator
import yaml

import filelock
import vedo


def range_include_stop(
    start: int,
    stop: int,
    step: int = 1,
) -> Iterator[int]:
    """Alternative to the python range() function which includes outputting the stop value"""
    # The python range function would normally exclued the
    # stop value. This function allows us to include the
    # stop value without adjusting the stop value to stop + step
    for i in range(start, stop, step):
        yield i
    # include stop if it would have been one of the steps
    if ((start - stop) % step) == 0:
        yield stop


def get_artefact_alignment_planes(
    artefact: vedo.Mesh,
) -> tuple[vedo.Plane, vedo.Plane, vedo.Plane]:
    """Make planes for all xy, xz, yz for viusalisations"""
    (
        breadth_min,
        breadth_max,
        length_min,
        length_max,
        thickness_min,
        thickness_max,
    ) = artefact.bounds()

    breadth = abs(breadth_max - breadth_min)
    length = abs(length_max - length_min)
    thickness = abs(thickness_max - thickness_min)

    breadth_pos = breadth_min + breadth / 2
    length_pos = length_min + length / 2
    thickness_pos = thickness_min + thickness / 2

    x_plane = vedo.Plane(
        pos=(0, length_pos, thickness_pos),
        normal=(1, 0, 0),
        s=(thickness, length),
        c="yellow",
        alpha=0.5,
    )

    z_plane = vedo.Plane(
        pos=(breadth_pos, length_pos, 0),
        normal=(0, 0, 1),
        s=(breadth, length),
        c="green",
        alpha=0.5,
    )

    y_plane = vedo.Plane(
        pos=(breadth_pos, 0, thickness_pos),
        normal=(0, 1, 0),
        s=(thickness, breadth),
        c="blue",
        alpha=0.5,
    )

    return x_plane, y_plane, z_plane


def output_csv_data(
    filepath: pathlib.Path,
    data_dict: dict,
):
    """Writes a dictionary to a file"""
    lock_file = filepath.with_suffix(filepath.suffix + ".lock")

    lock = filelock.FileLock(lock_file=lock_file)
    with lock:
        if not filepath.exists():
            out = open(filepath, "w", newline="", encoding="utf8")
            writer = csv.DictWriter(
                out, fieldnames=data_dict.keys(), quoting=csv.QUOTE_ALL
            )
            writer.writeheader()
        else:
            out = open(filepath, "a", newline="", encoding="utf8")
            writer = csv.DictWriter(
                out, fieldnames=data_dict.keys(), quoting=csv.QUOTE_ALL
            )

        writer.writerow(data_dict)
        out.close()

        if True:  # output the csv data to stdout if set to True
            stdout_writer = csv.DictWriter(
                sys.stdout, fieldnames=data_dict.keys(), quoting=csv.QUOTE_ALL
            )
            stdout_writer.writeheader()
            stdout_writer.writerow(data_dict)


def get_element_path(
    node: dict,
    prefix: pathlib.Path = None,
) -> Iterator[pathlib.Path]:
    """Reads a yaml file and builds a path from a heirarchical structure"""
    match node:
        case dict():
            for element in node:
                if prefix:
                    newprefix = pathlib.Path(prefix) / element
                else:
                    newprefix = pathlib.Path(element)
                yield from get_element_path(node[element], prefix=newprefix)
        case list():
            for element in node:
                yield from get_element_path(element, prefix=prefix)
        case str():
            output = pathlib.Path(prefix) / node
            yield (output)
        case _:
            pass  # excludes entries where the files are commented out


def setup_logging(
    config_file: pathlib.Path,
):
    """Configure logging using a config file"""

    with open(config_file, encoding="utf8") as f_in:
        config = yaml.safe_load(f_in)

    log_file = pathlib.Path(config["handlers"]["file"]["filename"])

    if not log_file.parent.exists():
        log_file.parent.mkdir(parents=True)

    logging.config.dictConfig(config)


if __name__ == "__main__":
    # TODO: add command line parsing to allow artefact processing from the command line

    exit()
