from . import ArtefactInfo
from . import ConstructionData
from . import ArtefactAnalysis
from . import ArtefactSegments

import numpy as np
import vedo

import matplotlib.pyplot as pyplot

from jinja2 import Environment, PackageLoader


def oriented_artefact_plot(
    artefact: vedo.Mesh,
    artefact_name: str,
    orientation_text: str,
):
    title = f"Oriented Artefact Plot: Dimensions for {artefact_name} Oriented {orientation_text}"
    plt = vedo.Plotter(title=title)
    plt.show(artefact, axes=7)

    return artefact.clone()


# The function below defines the Slices Plot. The original Artefact Slice is
# shown as a thick brown line, The Reference Mesh (Endo-/Mean-/Exo-Sym) slice is
# shown as a thick magenta/red/blue line. The X-axis mirrored face of the
# original artefact slice is shown as a thin green line. The mirrored side of
# the original artefact slice is shown as a thin orange line. The mirrored face
# and side of the original artefact slice is shown as a thin purple line.


def slices_plot(
    artefact: vedo.Mesh,
    artefact_info: ArtefactInfo,
    construction_data_list: list[ConstructionData],
):
    (
        breadth_min,
        breadth_max,
        length_min,
        length_max,
        thickness_min,
        thickness_max,
    ) = artefact.bounds()

    breadth_lim = abs(breadth_max - breadth_min) / 2
    thickness_lim = abs(thickness_max - thickness_min) / 2

    ylim_min, ylim_max = (-breadth_lim, breadth_lim)
    xlim_min, xlim_max = (-thickness_lim, thickness_lim)

    samples = artefact_info.samples

    # plot_type = construction_data.analysis_method.text

    slice_length_list = np.unique(samples.point.length)
    slice_length_list[::-1].sort()  # sort in descending order

    slice_count = slice_length_list.size

    fig, axs = pyplot.subplots(1, slice_count, sharey=True, figsize=(50, 7))

    legend_label = []
    fig.autofmt_xdate(rotation=90)
    for slice_number, slice_length in enumerate(slice_length_list):
        point_list_from_artefact_axis = samples[samples.point.length == slice_length]

        axs[slice_number].set_ylim(ylim_min * 1.1, ylim_max * 1.1)
        axs[slice_number].set_xlim(xlim_min * 1.1, xlim_max * 1.1)

        legend_label.append("Artefact Slice")
        axs[slice_number].plot(
            point_list_from_artefact_axis.point.thickness,
            point_list_from_artefact_axis.point.breadth,
            c="brown",
            linewidth=1,
        )

        if True:  # Plot the mirrored X-axis artefact slices
            legend_label.append("Mirror X-Axis")
            axs[slice_number].plot(
                -point_list_from_artefact_axis.point.thickness,
                point_list_from_artefact_axis.point.breadth,
                c="green",
                linewidth=1,
            )

        if True:  # Plot the mirrored Z-axis artefact slices
            legend_label.append("Mirror Z-Axis")
            axs[slice_number].plot(
                point_list_from_artefact_axis.point.thickness,
                -point_list_from_artefact_axis.point.breadth,
                c="orange",
                linewidth=1,
            )

        if True:  # Plot the mirrored X- and Z-axes artefact slices
            legend_label.append("Mirror X- & Z-Axes")
            axs[slice_number].plot(
                -point_list_from_artefact_axis.point.thickness,
                -point_list_from_artefact_axis.point.breadth,
                c="purple",
                linewidth=1,
            )

        for construction_data in construction_data_list:
            construction_samples = construction_data.sample_data

            plot_colour = construction_data.analysis_method.colour

            plot_points = construction_samples[
                construction_samples.point.length == slice_length
            ]

            if True:  # Plot the reference mesh slices
                legend_label.append(construction_data.analysis_method.text)
                axs[slice_number].plot(
                    plot_points.point.thickness,
                    plot_points.point.breadth,
                    c=plot_colour,
                    linewidth=2,
                )

        # TODO: Proper way to set orientation of xticks, but needs work using
        # fig.autofmt_xdate(rotation=90) as an interim
        axs[slice_number].set_xticks(axs[slice_number].get_xticks())
        axs[slice_number].set_xticklabels(
            axs[slice_number].get_xticklabels(), rotation=90, ha="center"
        )

    slice_count = len(artefact_info.original_slice_data)
    title = f"Defining the Geometry of the {construction_data.analysis_method.text} - Radial Distance from Y-Axis (0,0) for {slice_count} Crossectional Slices of {artefact_info.name} from Tip (Left) to Butt (Right)"
    fig.suptitle(title)
    fig.legend(
        list(dict.fromkeys(legend_label)),
        # ["Original", "Endo-Sym", "Exo-Sym", "Mean-Sym"],
        loc="upper center",
        bbox_to_anchor=(0.5, 0.945),
        ncol=7,
        fancybox=True,
        shadow=True,
    )
    fig.text(0.5, 0.04, "Z-Axis = Thickness (mm)", ha="center", va="center")
    fig.text(
        0.02,
        0.5,
        "X-Axis = Breadth (mm)",
        ha="center",
        va="center",
        rotation="vertical",
    )
    pyplot.subplots_adjust(
        left=0.048,
        bottom=0.14,
        right=0.979,
        top=0.864,
        wspace=0.19,
        hspace=None,
    )

    pyplot.show(block=True)


def segment_plot(
    artefact: vedo.Mesh,
    artefact_segments: ArtefactSegments,
):
    artefact_axes = vedo.Axes(artefact)
    title = "Bilateral Plot"
    vedo.Plotter(title=title).show(
        artefact.alpha(0.2),
        artefact_segments.left.c("yellow").alpha(0.4),
        artefact_segments.right.c("blue").alpha(0.4),
        artefact_axes,
    )
    title = "Bifacial Plot"
    vedo.Plotter(title=title).show(
        artefact.alpha(0.2),
        artefact_segments.dorsal.c("green").alpha(0.4),
        artefact_segments.ventral.c("red").alpha(0.4),
        artefact_axes,
    )
    title = "QI Ventral-Right Quadrant Plot"
    vedo.Plotter(title=title).show(
        artefact.alpha(0.2),
        artefact_segments.ventral_right.c("red").alpha(0.4),
        artefact_axes,
    )
    title = "QII Dorsal-Right Quadrant Plot"
    vedo.Plotter(title=title).show(
        artefact.alpha(0.2),
        artefact_segments.dorsal_right.c("yellow").alpha(0.4),
        artefact_axes,
    )
    title = "QIII Dorsal-Left Quadrant Plot"
    vedo.Plotter(title=title).show(
        artefact.alpha(0.2),
        artefact_segments.dorsal_left.c("green").alpha(0.4),
        artefact_axes,
    )
    title = "QIV Ventral-Left Quadrant Plot"
    vedo.Plotter(title=title).show(
        artefact.alpha(0.2),
        artefact_segments.ventral_left.c("blue").alpha(0.4),
        artefact_axes,
    )
    title = "Oriented Quadrants Plot"
    vedo.Plotter(title=title).show(
        artefact.alpha(0.2),
        artefact_segments.dorsal_right.c("red").alpha(0.4),
        artefact_segments.dorsal_left.c("green").alpha(0.4),
        artefact_segments.ventral_right.c("yellow").alpha(0.4),
        artefact_segments.ventral_left.c("blue").alpha(0.4),
        artefact_axes,
    )


def html_output(
    artefact_info: ArtefactInfo,
    artefact_segments: ArtefactSegments,
    construction_data: ConstructionData,
    artefact_analysis: ArtefactAnalysis,
) -> str:
    environment = Environment(loader=PackageLoader("lithikos", "templates/"))
    template = environment.get_template("sample_output.html")
    return template.render(
        artefact_info=artefact_info,
        artefact_segments=artefact_segments,
        construction_data=construction_data,
        artefact_analysis=artefact_analysis,
    )


def txt_output(
    artefact_info: ArtefactInfo,
    artefact_segments: ArtefactSegments,
    construction_data: ConstructionData,
    artefact_analysis: ArtefactAnalysis,
) -> str:
    environment = Environment(loader=PackageLoader("lithikos", "templates/"))
    template = environment.get_template("sample_output.txt")
    return template.render(
        artefact_info=artefact_info,
        artefact_segments=artefact_segments,
        construction_data=construction_data,
        artefact_analysis=artefact_analysis,
    )
