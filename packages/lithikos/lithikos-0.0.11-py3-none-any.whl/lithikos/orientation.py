from . import OrientationMethod

import vedo
import trimesh
import numpy as np


def identify_tip_vertices(artefact: vedo.Mesh) -> np.ndarray:
    # get the furthest point from the centre of mass

    vertices = artefact.vertices
    centre = get_volumetric_centre(artefact)

    distance_to_centre_of_mass = np.sqrt(np.sum((vertices - centre) ** 2, axis=1))

    tip_index_list = np.argmax(distance_to_centre_of_mass)

    tip_vertices = vertices[tip_index_list]

    return tip_vertices


def get_end_points(artefact: vedo.Mesh) -> tuple[np.ndarray, np.ndarray]:
    vertices = artefact.vertices

    tip_vertices = identify_tip_vertices(artefact=artefact)

    vertices = artefact.vertices

    distance_to_tip = np.sqrt(np.sum((vertices - tip_vertices) ** 2, axis=1))

    butt_index_list = np.argmax(distance_to_tip)

    butt_vertices = vertices[butt_index_list]

    return tip_vertices, butt_vertices


def get_volumetric_centre(artefact: vedo.Mesh):
    points = artefact.vertices
    faces = artefact.cells

    mesh = trimesh.Trimesh(vertices=points, faces=faces)

    return mesh.center_mass


def get_centre_of_point_cloud(artefact: vedo.Mesh):
    return artefact.center_of_mass()


def move_tip_to_origin(artefact: vedo.Mesh) -> vedo.Mesh:
    # get the furthest point from the centre of mass

    temp = artefact.clone()

    artefacts = []
    artefacts.append(artefact.clone().c("red").alpha(0.5))

    vertices = artefact.vertices
    centre = get_volumetric_centre(artefact)

    distance_to_centre_of_mass = np.sqrt(np.sum((vertices - centre) ** 2, axis=1))

    tip_index_list = np.argmax(distance_to_centre_of_mass)

    tip_vertices = vertices[tip_index_list]

    temp.align_with_landmarks(
        [tip_vertices, centre],
        [[0, 0, 0], [0, -distance_to_centre_of_mass.max(), 0]],
        rigid=True,
    )

    artefacts.append(temp.clone().c("green").alpha(0.5))
    if False:
        plt = vedo.Plotter()
        plt.show(artefacts, axes=True)

    artefact = temp.clone()

    return artefact


def orient_tip_to_centre_of_mass(artefact: vedo.Mesh) -> vedo.Mesh:
    return_artefact = artefact.clone()

    tip_mean, butt_mean = get_end_points(artefact=return_artefact)

    origin = np.asarray((0, 0, 0))

    com = get_volumetric_centre(return_artefact)

    r = np.sqrt(((tip_mean - com) ** 2).sum())

    new_com = [0, -r, 0]
    return_artefact.align_with_landmarks([tip_mean, com], [origin, new_com])

    if False:
        xt, yt, zt = tip_mean
        # xb, yb, zb = com

        p0_y = yt + 50
        p1_y = butt_mean[1] - 50
        axis_line = vedo.Line(p0=(0, p0_y, 0), p1=(0, p1_y, 0))
        plt = vedo.Plotter()
        plt.show(return_artefact.c("blue"), artefact.alpha(0.3), axis_line, axes=True)

    return return_artefact.clone()


def orient_tip_to_centre_of_hollow_mesh(artefact: vedo.Mesh) -> vedo.Mesh:
    return_artefact = artefact.clone()

    tip_mean, butt_mean = get_end_points(artefact=return_artefact)

    origin = np.asarray((0, 0, 0))

    com = get_centre_of_point_cloud(return_artefact)

    r = np.sqrt(((tip_mean - com) ** 2).sum())

    new_com = [0, -r, 0]
    return_artefact.align_with_landmarks([tip_mean, com], [origin, new_com])

    if False:
        xt, yt, zt = tip_mean
        # xb, yb, zb = com

        p0_y = yt + 50
        p1_y = butt_mean[1] - 50
        axis_line = vedo.Line(p0=(0, p0_y, 0), p1=(0, p1_y, 0))
        plt = vedo.Plotter()
        plt.show(return_artefact.c("blue"), artefact.alpha(0.3), axis_line, axes=True)

    return return_artefact.clone()


def orient_tip_to_butt(artefact: vedo.Mesh) -> vedo.Mesh:
    return_artefact = artefact.clone()

    tip_mean, butt_mean = get_end_points(artefact=return_artefact)

    origin = np.asarray((0, 0, 0))

    r = np.sqrt(((tip_mean - butt_mean) ** 2).sum())

    new_butt = [0, -r, 0]
    return_artefact.align_with_landmarks([tip_mean, butt_mean], [origin, new_butt])

    return return_artefact.clone()


def orient_to_fitline(artefact: vedo.Mesh) -> vedo.Mesh:
    # start with tip at origin for correct orientation
    return_artefact = move_tip_to_origin(artefact=artefact).clone()

    orienting_artefact = return_artefact.clone().decimate_pro(fraction=0.1)

    vertices = orienting_artefact.vertices
    # TODO: handle crash with non decimated artefact this uses lots of memory
    # and takes a long time if the following line causes a crash try decimating
    # the mesh before running the analysis
    fitline = vedo.fit_line(vertices)

    points = return_artefact.intersect_with_line(fitline)
    a = points[points[:, 1].argsort()][::-1]

    com = return_artefact.center_of_mass()

    tip_intersect = a[0]
    butt_intersect = a[-1]

    rt = np.sqrt(((tip_intersect - com) ** 2).sum())
    rb = np.sqrt(((butt_intersect - com) ** 2).sum())

    if rb > rt:
        tip_intersect, butt_intersect = butt_intersect, tip_intersect

    r = np.sqrt(((tip_intersect - butt_intersect) ** 2).sum())

    new_butt = [0, -r, 0]
    return_artefact.align_with_landmarks(
        [tip_intersect, butt_intersect], [(0, 0, 0), new_butt]
    )

    if False:
        plt = vedo.Plotter()
        plt.show(return_artefact.c("blue"), artefact, axes=True)

    return return_artefact.clone()


def align_thickness_with_x_axis(artefact: vedo.Mesh) -> vedo.Mesh:
    xmin, xmax, ymin, ymax, zmin, zmax = artefact.bounds()

    artefacts = []
    artefacts.append(artefact.clone().c("red"))

    vertices = artefact.vertices
    distance_to_y_axis = (vertices[:, 0] ** 2 + vertices[:, 2] ** 2) ** 0.5
    opposites = vertices[:, 2]
    adjacents = vertices[:, 0]
    angles_from_x = np.arctan(opposites / adjacents)

    furthest_point_index = np.argwhere(distance_to_y_axis == max(distance_to_y_axis))

    this_angle = angles_from_x[furthest_point_index.max()]

    artefact.rotate_y(this_angle, rad=True)
    artefacts.append(artefact.clone().c("yellow"))

    vertices = artefact.vertices

    max_x_value = vertices[:, 0].max()
    min_x_value = vertices[:, 0].min()

    max_x_list = vertices[vertices[:, 0] == max_x_value]
    min_x_list = vertices[vertices[:, 0] == min_x_value]

    r = 0
    x_min = None
    x_max = None

    for min_x in min_x_list:
        for max_x in max_x_list:
            this_r = abs(max_x[0] - min_x[0])
            if this_r > r:
                x_min = min_x
                x_max = max_x

    adjacent = x_max[0] - x_min[0]
    opposite = x_max[2] - x_min[2]

    widest_points_average_y_value = (x_max[1] + x_min[1]) / 2
    theta = np.arctan(opposite / adjacent)

    artefact.rotate_y(theta, rad=True)

    # Setting this to true will orient artefact using widest part as closest to
    # butt
    if False:
        artefact_length = abs(ymax - ymin)
        artefact_half_way = -artefact_length / 2

        if artefact_half_way <= widest_points_average_y_value:
            artefact.rotate_z(np.pi, rad=True)

    artefacts.append(artefact.clone().c("green"))

    return artefact.clone()


def orient_artefact(
    artefact: vedo.Mesh,
    artefact_name: str,
    orientation_method: OrientationMethod,
) -> vedo.Mesh:
    artefacts = []

    # artefacts.append(artefact.clone().c("red"))

    if orientation_method is OrientationMethod.ORIENT_TIP_TO_BUTT:
        artefact = orient_tip_to_butt(artefact=artefact)
        artefacts.append(artefact.clone().c("yellow"))

    elif orientation_method is OrientationMethod.ORIENT_TIP_TO_COM:
        artefact = orient_tip_to_centre_of_mass(artefact=artefact)
        artefacts.append(artefact.clone().c("yellow"))

    elif orientation_method is OrientationMethod.ORIENT_TIP_TO_COHM:
        artefact = orient_tip_to_centre_of_hollow_mesh(artefact=artefact)
        artefacts.append(artefact.clone().c("yellow"))

    elif orientation_method is OrientationMethod.ORIENT_TO_FITLINE:
        artefact = orient_to_fitline(artefact=artefact)
        artefacts.append(artefact.clone().c("yellow"))

    artefact = align_thickness_with_x_axis(artefact=artefact)
    artefacts.append(artefact.clone().c("blue"))

    centre = get_volumetric_centre(artefact)

    artefact = artefact.shift(dy=-centre[1]).clone()

    artefacts.append(artefact.clone().c("green"))

    return artefact.clone()
