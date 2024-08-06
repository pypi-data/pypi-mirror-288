"""Contains command line invocation implementation for lithikos"""

import argparse
import importlib.resources
import pathlib
import glob

import vedo

# import lithikos.configs

from . import AnalysisMethod
from . import OrientationMethod
from . import SampleParameters
from . import process
from . import utils
from . import configs


LOGGING_CONFIG_FILE_NAME = "stderr-file.yaml"

ARTEFACT_DATA_FILE_NAME = "artefact_data.csv"

REFERENCE_DATA_FILE_NAME = "reference_data.csv"


def main():
    """Contains command line invocation implementation for lithikos"""

    cfg_file_resource = importlib.resources.files(package=configs)

    logging_config_file = cfg_file_resource / LOGGING_CONFIG_FILE_NAME

    utils.setup_logging(config_file=logging_config_file)

    p = pathlib.Path(".")

    output_root = pathlib.Path("output")
    quadrant_subdir = pathlib.Path("quadrants")

    analysis_method_choices = [method.text for method in AnalysisMethod]
    orientation_method_choices = [method.text for method in OrientationMethod]

    parser = argparse.ArgumentParser(
        prog="lithikos",
        description="""
        Orients 3D models of stone artefacts, isolates quadrants
        about the long axis of the tool, measures artefact surface area and
        artefact/quadrant volumes and dimensions, samples artefact model geometry,
        synthesises radially symmetrical reference meshes, and delivers oriented
        artefact/quadrant models, symmetrical reference models, and artefact_data.csv
        and reference_data.csv files""",
        epilog="Thank you for using lithikos",
    )

    parser.add_argument(
        "filenames",
        help="""
        One or more files containing mesh objects in Wavefront (obj) format""",
        nargs=argparse.ONE_OR_MORE,
    )

    parser.add_argument(
        "--orientation-method",
        choices=orientation_method_choices,
        nargs=argparse.ONE_OR_MORE,
        default=(OrientationMethod.ORIENT_TIP_TO_COM.text,),
    )

    parser.add_argument(
        "--analysis-method",
        choices=analysis_method_choices,
        nargs=argparse.ONE_OR_MORE,
        default=(AnalysisMethod.ENDO_SYM.text,),
    )

    parser.add_argument(
        "--slice-count",
        type=int,
        default=100,
    )

    parser.add_argument(
        "--point-count",
        type=int,
        default=36,
    )

    parser.add_argument("--tip-spacing", type=float, default=0.001)

    parser.add_argument("--butt-spacing", type=float, default=0.001)

    args = parser.parse_args()

    sample_parameters = SampleParameters(
        slice_count=args.slice_count,
        point_count=args.point_count,
        tip_spacing=args.tip_spacing,
        butt_spacing=args.butt_spacing,
    )

    orientation_methods = [
        OrientationMethod.from_text(method) for method in args.orientation_method
    ]
    analysis_methods = [
        AnalysisMethod.from_text(method) for method in args.analysis_method
    ]

    sample_parameters_list = [sample_parameters]

    for filename in args.filenames:
        artefact_paths = [pathlib.Path(p) for p in glob.glob(filename)]

        for artefact_path in artefact_paths:
            artefact_name = artefact_path.stem

            parent_dir = artefact_path.parent.name

            output_dir = output_root / parent_dir

            output_dir.mkdir(parents=True, exist_ok=True)

            original_artefact = vedo.Mesh(artefact_path.as_posix()).clean()

            artefact_data_file = p / pathlib.Path(ARTEFACT_DATA_FILE_NAME)
            reference_data_file = p / pathlib.Path(REFERENCE_DATA_FILE_NAME)

            process.process(
                original_artefact=original_artefact,
                artefact_name=artefact_name,
                output_dir=output_dir,
                orientation_methods=orientation_methods,
                analysis_methods=analysis_methods,
                sample_parameters_list=sample_parameters_list,
                artefact_data_file=artefact_data_file,
                reference_data_file=reference_data_file,
                quadrant_subdir=quadrant_subdir,
            )


if __name__ == "__main__":
    main()
