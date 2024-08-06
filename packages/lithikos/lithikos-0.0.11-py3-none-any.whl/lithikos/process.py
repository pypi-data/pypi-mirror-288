import pathlib
import vedo

from . import OrientationMethod
from . import AnalysisMethod
from . import SampleParameters
from . import ArtefactSegments
from . import ConstructionData
from . import ArtefactInfo
from . import QuadrantMeasurements
from . import ArtefactAnalysis
from . import Scale
from . import utils
from . import sampling
from . import analysis

from . import orientation
from . import construction
from . import plotting

from . import logger


def process(
    original_artefact: vedo.Mesh,
    artefact_name: str,
    output_dir: pathlib.Path,
    orientation_methods: list[OrientationMethod],
    analysis_methods: list[AnalysisMethod],
    sample_parameters_list: SampleParameters,
    quadrant_subdir: pathlib.Path,
    artefact_data_file: pathlib.Path,
    reference_data_file: pathlib.Path,
):
    logger.info(
        "Processing artefact: %s",
        artefact_name,
    )
    for orientation_method in orientation_methods:
        orientation_abbr = orientation_method.abbreviation
        orientation_text = orientation_method.text

        logger.info(
            "Processing artefact: %s orientation %s",
            artefact_name,
            orientation_text,
        )

        oriented_artefact_identifier = f"{artefact_name}_{orientation_abbr}"

        oriented_mesh_file_name = f"{oriented_artefact_identifier}_3D-model.obj"
        oriented_mesh_full_file_name = output_dir / oriented_mesh_file_name

        print(oriented_mesh_full_file_name)

        oriented_artefact = orientation.orient_artefact(
            artefact=original_artefact,
            artefact_name=artefact_name,
            orientation_method=orientation_method,
        )

        # If True, this displays the Oriented Artefact Plot with Model Volume
        # and dimensions.

        if False:
            plotting.oriented_artefact_plot(
                artefact=oriented_artefact,
                artefact_name=artefact_name,
                orientation_text=orientation_text,
            )

        (
            breadth_min,
            breadth_max,
            length_min,
            length_max,
            thickness_min,
            thickness_max,
        ) = oriented_artefact.bounds()

        initial_columns = {
            "Artefact_ID": artefact_name,
            "Orientation_Type": orientation_text,
        }

        if False:  # Setting this will calculate the dimension data then end
            continue

        vedo.write(oriented_artefact, oriented_mesh_full_file_name.as_posix())

        if False:
            read_artefact = vedo.Mesh(oriented_mesh_full_file_name.as_posix())
            print(
                f"""original vol: {original_artefact.volume()
                } oriented vol:{oriented_artefact.volume() } read
                vol:{read_artefact.volume()}"""
            )

        oriented_artefact_segments = ArtefactSegments(oriented_artefact)

        quadrant_measurements = QuadrantMeasurements(
            artefact_segments=oriented_artefact_segments,
        )
        artefact_data = (
            initial_columns
            | {
                "Artefact_Surface_Area": oriented_artefact.area() * Scale.AREA,
            }
            | quadrant_measurements.to_volume_data_dict()
        )

        utils.output_csv_data(
            filepath=artefact_data_file,
            data_dict=artefact_data,
        )

        quadrant_output_dir = output_dir / quadrant_subdir

        # TODO: handle error cases
        if not quadrant_output_dir.exists():
            quadrant_output_dir.mkdir(parents=True)
        segment_map = {
            # f'{oriented_artefact_identifier}-face-V.obj':
            #    oriented_artefact_segments.ventral,
            # f'{oriented_artefact_identifier}-face-D.obj':
            #    oriented_artefact_segments.dorsal,
            # f'{oriented_artefact_identifier}-side-R.obj':
            #    oriented_artefact_segments.right,
            # f'{oriented_artefact_identifier}-side-L.obj':
            #    oriented_artefact_segments.left,
            f"{oriented_artefact_identifier}-QI_VR.obj": oriented_artefact_segments.ventral_right,
            f"{oriented_artefact_identifier}-QII_DR.obj": oriented_artefact_segments.dorsal_right,
            f"{oriented_artefact_identifier}-QIII_DL.obj": oriented_artefact_segments.dorsal_left,
            f"{oriented_artefact_identifier}-QIV_VL.obj": oriented_artefact_segments.ventral_left,
        }
        for name, segment in segment_map.items():
            segment_file = quadrant_output_dir / name
            vedo.write(segment, segment_file.as_posix())

        if False:
            # plot segments
            plotting.segment_plot(
                artefact=oriented_artefact,
                artefact_segments=oriented_artefact_segments,
            )

        sample_parameters: SampleParameters
        for sample_parameters in sample_parameters_list:
            artefact_info: ArtefactInfo

            artefact_info = sampling.get_artefact_samples(
                artefact=oriented_artefact,
                sample_parameters=sample_parameters,
            )
            artefact_info.name = artefact_name

            construction_data_list: list[ConstructionData]

            construction_data_list = []
            for analysis_method in analysis_methods:
                construction_data = analysis.analyse_artefact_samples(
                    artefact_info=artefact_info,
                    analysis_method=analysis_method,
                )
                construction_data_list.append(construction_data)

            artefact_info.orientation_method = orientation_method

            slice_count = sample_parameters.slice_count
            point_count = sample_parameters.point_count
            tip_spacing = sample_parameters.tip_spacing
            butt_spacing = sample_parameters.butt_spacing

            analysis_info_text = f"{slice_count.text}-{point_count.text}"
            spacing_info_text = f"{tip_spacing.text}-{butt_spacing.text}"

            if False:
                # This code displays the Slices Plot.
                plotting.slices_plot(
                    artefact=oriented_artefact,
                    artefact_info=artefact_info,
                    construction_data_list=construction_data_list,
                )

            for construction_data in construction_data_list:
                analysis_type = construction_data.analysis_method

                analysis_type_abbr = analysis_type.abbreviation

                analysis_type_text = analysis_type.text

                mesh_colour = analysis_type.colour

                analysis_detail_text = f"{analysis_info_text}_{spacing_info_text}"

                constructed_mesh_file_name = f"{oriented_artefact_identifier}_{analysis_type_abbr}_{analysis_detail_text}.obj"
                html_output_file_name = f"{oriented_artefact_identifier}_{analysis_type_abbr}_{analysis_detail_text}_out.html"
                txt_output_file_name = f"{oriented_artefact_identifier}_{analysis_type_abbr}_{analysis_detail_text}_out.txt"

                sample_constructed_mesh = construction.create_mesh_from_point_data(
                    construction_data
                )

                constructed_result = sample_constructed_mesh

                artefact_analysis = ArtefactAnalysis(
                    artefact_segments=oriented_artefact_segments,
                    constructed_result=constructed_result,
                )
                # If set to True, this code displays the final Reference Mesh
                # Plot before printing the Results to the Terminal.

                if False:
                    title = constructed_mesh_file_name
                    plt = vedo.Plotter(title=title)
                    plt.show(
                        constructed_result.mesh.alpha(0.3).c(mesh_colour),
                    )

                constructed_result.mesh.c(mesh_colour)

                reference_data = (
                    initial_columns
                    | sample_parameters.to_csv_dict_data()
                    | {
                        "Analysis_Type": analysis_type_text,
                    }
                    | {
                        "Reference_Volume": constructed_result.mesh.volume()
                        * Scale.VOLUME,
                    }
                )

                utils.output_csv_data(
                    filepath=reference_data_file,
                    data_dict=reference_data,
                )

                html_output = plotting.html_output(
                    artefact_info=artefact_info,
                    artefact_segments=oriented_artefact_segments,
                    construction_data=construction_data,
                    artefact_analysis=artefact_analysis,
                )

                html_output_full_file_name = output_dir / html_output_file_name

                with open(html_output_full_file_name, "w", encoding="utf-8") as file:
                    file.write(html_output)

                txt_output = plotting.txt_output(
                    artefact_info=artefact_info,
                    artefact_segments=oriented_artefact_segments,
                    construction_data=construction_data,
                    artefact_analysis=artefact_analysis,
                )

                txt_output_full_file_name = output_dir / txt_output_file_name

                with open(txt_output_full_file_name, "w", encoding="utf-8") as file:
                    file.write(txt_output)

                print(txt_output)
                # print(f'Generated mesh has {clean_mesh.npoints} vertices and
                # {clean_mesh.ncells} faces!')
                constructed_mesh_full_file_name = (
                    output_dir / constructed_mesh_file_name
                )
                vedo.write(
                    constructed_result.mesh, constructed_mesh_full_file_name.as_posix()
                )
