"""
Evaluating Handaxe Bilateral/Bifacial Mirror Symmetry Along the Primary Axis in
3D

Any solid bifurcated by a plane along its primary axis can be split into two
shapes (in this case left and right halves or ventral and dorsal faces) with
equivalent volumes, but both halves may take an infinite number of shapes while
sharing the primary plane of reflection (the long axes), thus nullifying the
claim that correlated volumes of bifurcated stone tools can be used as a valid
warrant in the analoyses of mirror symmetry. In order for a particular volume to
act as a valid warrant for mirror symmetry, it must reference a known
symmetrical volume. In order to evaluate bilateral and bifacial mirror
symmetries in reference to the long axis (i.e., the Y-axis), this analyzer
generates a known symmetrical mesh within a shared analysis space oriented to
the same axes as the stone tool. The analysis assumes that a bifacially and
bilaterally symmetrical mesh generated to fit within (the Endo-Sym) or encompass
(the Exo-Sym) the artefact provides the necessary symmetrical reference to
warrant a volume-based analysis of mirror (reflection) symmetry, under the
assumption that within the same analysis space and oriented to the same axes,
any volume occupying the space beyond the surface of the Endo-Sym and beneath
the surface of the Exo-Sym is due to asymmetry inherent in the artefact.

Though the analyses are performed with the artefact in plan view (tip up, butt
down), to better visualize an evaluation of bilateral and bifacial mirror
symmetry, the tip of the artefact is rotated around the X-axis by -90 degrees in
the Z-plane to provide a bottom view of the artefact, with the butt centered,
the ventral or front face of the artefact pointing upwards, and the dorsal or
rear face pointing downwards. This bottom view displays the Z-plane vertically
and the X-plane horizontally, allowing for the simultaneous orthogonal
visualization of both the bilateral left (- X) and right (+ X) sides of the
artefact as well as the bifacial ventral (+ Z) and dorsal (-Z) faces. As the
reference mesh is symmetrical in both bilateral and bifacial aspects, each of
its quadrants are equivalent in volume occupying 1/4 the total volume of the
reference mesh. In bottom view, QI contains the ventral-right quadrant, QII the
dorsal-right quadrant, QIII the dorsal-left quadrant, and QIV the ventral left
quadrant.

To begin, the artefact is bifucated into quadrants by collapsing the artefact
mesh around the X and Z planes in each quadrant. From this perspetive bilateral
or left/right mirror asymmetry can be calculated by isolating opposing volumes
across the plane of reflective symmtery, in bilateral case the Z-plane. To
isolate the artefact's volumetric asymmetry in each quadrant, we determine the
difference between the quadrant's reference volume and the artefact's quadrant
(or segment) volume. For an Endo-Sym analysis, the reference mesh's quarant
volume is subtracted from the artefact's quadrant volume. For an Exo-Sym
analysis, the artefact's quadrant volume is subtracted from the reference mesh's
quadrant volume. In both cases, the remainder is the artefact's volumetric
asymmetry for that quadrant. To calculate bilateral mirror (reflective)
asymmetry across the Z-plane, each face must be analyzed separately, as it
contains both a ventral and a dorsal component. During an analysis of bilateral
mirror symmetry, a comparison of the artefact's  is made In the context of a
volumetric ananlysis refers to the difference between the volume of a
particualar artefact quadrant and the volume of the known symmetrical reference
quadrant in relation to the long axis.

Begining with QI (or the dorsal-right quadrant), the volume of the
known-symmetrical reference mesh is subtracted from the volume of the artefact
model to isolate the artefact's QI or dorsal-right asymmetric volume, also
refered to as the artefact's dorsal-right asymmetry, which is contained in the
variable 'bilateral_dorsal_right_asymmetric_volume'. The same process is
performed in quadrants QII, QIII, and QIV to produce equivalent variables
containing their associated volumetric assymetries.

Next a series of bilateral ventral and dorsal asymmetry coefficients are
calculated based on opposing artefact asymmetries. First the
bilateral_ventral_asymmetry_coefficient is calculated by comparing the
ventral_left_asymmetric_volume to the ventral_right_asymmentric_volume then
dividing the samller volume by the larger. This process is repeated across the
Z-plane to calculate the bilateral_dorsal_asymmetry_coefficient, wherein the
dorsal_left_asymmetric_volume is compared to the
dorsal_right_asymmentric_volume, and the samller volume is divided by the larger
to produce the bilateral_dorsal_asymmetry_coefficient.

An equivalent approach is taken to determine the bifacial left and right
asymmetry coefficients, wherein the dorsal_left_asymmetric_volume is compared to
the dorsal_right_asymmentric_volume, and the samller volume is divided by the
larger to produce the bifacial_left_asymmetry_coefficient. Next the
ventral_left_asymmetric_volume is compared to the
ventral_right_asymmentric_volume, and the samller volume is divided by the
larger to produce the bifacial_right_asymmetry_coefficient.

# Bilateral VENTRAL and DORSAL COEFFICIENTS for COEFFICIENTS APPROACH

Evaluating Handaxe Bilateral/Bifacial Mirror Symmetry Along the Primary Axis in
3D

While any solid bifurcated by a plane along its primary axis can be split into
two shapes (in this case left and right halves or ventral and dorsal faces) with
equivalent volumes, importantly both halves may take an infinite number of
shapes while sharing the primary plane of reflection (the long axis), thus
nullifying the claim that correlated volumes of bifurcated stone tools can be
used as a valid warrant in the analyses of mirror symmetry.

For a particular volume to act as a valid warrant for mirror symmetry, it must
reference a known symmetrical volume. To evaluate bilateral and bifacial mirror
symmetries in reference to the long axis (i.e., the Y-axis), this analyzer
generates a known symmetrical mesh within a shared analysis space oriented to
the same axes as the stone tool. The analysis assumes that a bifacially and
bilaterally symmetrical mesh generated to fit within (the Endo-Sym) or encompass
(the Exo-Sym) the artefact provides the necessary symmetrical reference to
warrant a volume-based analysis of mirror (reflection) symmetry, under the
assumption that within the same analysis space and oriented to the same axes,
any volume occupying the space beyond the surface of the Endo-Sym and beneath
the surface of the Exo-Sym is due to asymmetry inherent in the artefact.

Though the analyses are performed with the artefact in plan view (tip up, butt
down), to better visualize an evaluation of bilateral and bifacial mirror
symmetry, the tip of the artefact is rotated around the X-axis by 270 degrees in
the Z-plane to provide a bottom view of the artefact, with the butt centered,
the ventral or front face of the artefact pointing upwards, and the dorsal or
rear face pointing downwards. This bottom view displays the Z-plane vertically
and the X-plane horizontally, allowing for the simultaneous orthogonal
visualization of both the bilateral left (- X) and right (+ X) sides of the
artefact as well as the bifacial ventral (+ Z) and dorsal (-Z) faces. As the
reference mesh is symmetrical in both bilateral and bifacial aspects, each of
its quadrants are equivalent in volume occupying 1/4 the total volume of the
reference mesh. In bottom view, QI contains the ventral-right quadrant, QII the
dorsal-right quadrant, QIII the dorsal-left quadrant, and QIV the ventral-left
quadrant.

To begin, the artefact is bifurcated into quadrants by collapsing its mesh to
the X and Z planes in each quadrant. From this perspective bilateral or
left/right mirror asymmetry can be calculated by isolating opposing volumes
across the plane of reflective symmetry, in the bilateral case the Z-plane. To
isolate the artefact's volumetric asymmetry in each quadrant, we determine the
difference between the quadrant's reference mesh volume and the artefact's
quadrant (referred to in the code as a segment) volume.

For an Endo-Sym analysis, the reference mesh's quadrant volume is subtracted
from the artefact's quadrant volume. For an Exo-Sym analysis, the artefact's
quadrant volume is subtracted from the reference mesh's quadrant volume. In both
cases, the remainder is the artefact's volumetric asymmetry for that quadrant.

To calculate bilateral mirror (reflective) asymmetry across the Z-plane, each
face must be analyzed separately, as bilateral mirror symmetry contains both a
ventral and a dorsal component. During an Endo-Sym analysis of bilateral mirror
symmetry, a comparison of the artefact's remaining asymmetry volume is compared
to the same volume in the opposing quadrant across the plane of symmetry, in
this case the Z plane. First, to determine the ventral contribution to bilateral
mirror symmetry, the artefact's QI ventral-right volumetric asymmetry is
compared its QIV ventral-left counterpart, and the smaller volume is divided by
the larger volume to produce the artefact's ventral asymmetry coefficient. The
same process is repeated for the dorsal contribution to bilateral mirror
symmetry, wherein the remaining asymmetry volumes of the artefact's dorsal-right
and dorsal-left quadrants (QII and QIII) are compared. The smaller asymmetry
volume is then divided by the larger asymmetry volume to produce the artefact's
dorsal asymmetry coefficient. Both the ventral and dorsal coefficients of
bilateral symmetry are displayed in the Results printed to the Terminal at the
end of the analysis. To achieve the final coefficient of bilateral symmetry, the
ventral and dorsal coefficients are combined into various ratios by dividing the
smaller value by the larger value: the arithmetic mean, the weighted average,
the geometric mean, the harmonic mean, and the root-mean-square. The analyst can
then choose the ratio which best fits the current research question.

Bifacial mirror symmetry is determined by substituting the appropriate remaining
artefact asymmetry volumes to calculate bifacial mirror symmetry across the X
plane. First the asymmetry volumes for QI ventral-right quadrant and QII
dorsal-right are compared. The smaller asymmetry volume is divided by the larger
to determine the right-hand coefficient of bifacial symmetry. The left-hand
coefficient of bifacial symmetry is determined by comparing the artefact's
remaining asymmetry volumes located in the QIII dorsal-left and QIV ventral-left
quadrants. The smaller asymmetry volume is divided by the larger asymmetry
volume to determine the artefact's left-hand coefficient of bifacial symmetry.
Both the left- and right-hand coefficients of bifacial symmetry are displayed in
the Results printed to the Terminal at the end of the analysis. To achieve the
final coefficient of bifacial symmetry, the left- and right-hand coefficients
are combined into the same five ratios offered for bilateral coefficient of
symmetry, with the analyst choosing the ratio appropriate to the research
question.

For Exo-Sym analyses, the equations are modified to achieve an equivalent ratio
between 0 and 1 as the final coefficient of bilateral/bifacial symmetry
described above. Namely, the artefact's asymmetry is now represented by
subtracting the smaller volume of the artefact's segment quadrant from the
larger volume of the Exo-Sym encompassing it. As the Exo-Sym represents the
smallest bilaterally/bifacially symmetrical mesh that can encompass the
artefact, any differences in volume are attributed to asymmetries inherent in
the artefact.

"""

import dataclasses

from . import Scale
from . import ConstructedResult
from . import ArtefactSegments


def calculate_asymmetry_coefficient_of(
    vol_1: float,
    vol_2: float,
) -> float:
    """
    This function determines the value of asymmetry_coefficients by evaluating
    the relationship between two asymmetric_volumes.
    """

    asymmetry_coefficient = min(vol_1, vol_2) / max(vol_1, vol_2)
    return asymmetry_coefficient


@dataclasses.dataclass
class MirrorSymmetry:
    """
    The MirrorSymmetry class uses the current values in asymmetry_coefficient_1
    and asymmetry_coefficient_2 to calculate_bilateral/bifacial mirror_symmetry.
    """

    asymmetry_coefficient_1: float
    asymmetry_coefficient_2: float

    # The following properties define the functions used to calcuate 5 different
    # ratios representing the final bilateral/bifacial_mirror_symmetry
    # coefficients.

    @property
    def arithmetic_mean(self):
        """
        The arithmetic_mean() function returns the arithmetic mean of the two
        asymmetry_coefficients as the final bilateral/bifacial_mirror_symmetry
        coefficient.
        """
        return (self.asymmetry_coefficient_1 + self.asymmetry_coefficient_2) / 2

    @property
    def weighted_average(self):
        """
        The weighted_average() function returns the weighted average of the two
        asymmetry_coefficients as the final bilateral/bifacial_mirror_symmetry
        coefficient.

        This ratio is appropraite if one asymmetry_coefficient or another is
        deemed more significant or reliable for an analysis of symmetry.
        """
        return (
            (self.asymmetry_coefficient_1 * 1) + (self.asymmetry_coefficient_2 * 1)
        ) / (1 + 1)

    @property
    def geometric_mean(self):
        """
        The geometric_mean() function returns the geometric mean of the two
        asymmetry_coefficients.

        This ratio is appropriate if one asymmetry_coefficient varies in scale
        over the other asymmetry_coefficient.
        """
        return (
            abs(self.asymmetry_coefficient_1) * abs(self.asymmetry_coefficient_2)
        ) ** 0.5

    @property
    def harmonic_mean(self):
        """
        The harmonic_mean() function returns the harmonic mean of the two
        asymmetry_coefficients.

        This ratio is sensitive to smaller values and may be useful if smaller
        values of symmetry are important to your analysis.
        """
        return 2 / (
            (1 / self.asymmetry_coefficient_1) + (1 / self.asymmetry_coefficient_2)
        )

    @property
    def rms(self):
        """
        The rms() function returns the root-mean-square of the two
        asymmetry_coefficients.

        This ratio gives more weight to larger values of symmetry if they are
        important for your analysis.
        """
        return (
            ((self.asymmetry_coefficient_1**2) + (self.asymmetry_coefficient_2**2)) / 2
        ) ** 0.5


@dataclasses.dataclass
class ArtefactAnalysis:
    constructed_result: (
        ConstructedResult  # Attribute storing information about constructed result
    )
    artefact_segments: (
        ArtefactSegments  # Attribute storing information about artefact segments
    )

    def __post_init__(self):
        """
        Post-initialization method to calculate additional attributes after the
        object is created.
        """

        # Calculating the volume of the constructed reference mesh and storing
        # it in a variable.
        self.reference_mesh_volume: float = self.constructed_result.mesh.volume()

        # Calculating the original artefact model volume and storing it in a
        # variable.
        self.original_artefact_volume: float = self.artefact_segments.artefact.volume()

        # HEMISPHERIC APPROACH

        # Calculating half of the constructed reference mesh volume and storing
        # it in a variable.
        self.diagnostic_hemisphere_volume: float = self.reference_mesh_volume / 2

        # Calculating the dorsal asymmetric volume and storing it in a variable.
        self.dorsal_asymmetric_volume: float = (
            self.artefact_segments.dorsal.volume() - self.diagnostic_hemisphere_volume
        )

        # Calculating the ventral asymmetric volume and storing it in a
        # variable.
        self.ventral_asymmetric_volume: float = (
            self.artefact_segments.ventral.volume() - self.diagnostic_hemisphere_volume
        )
        # Calculating the left asymmetric volume and storing it in a variable.
        self.left_asymmetric_volume: float = (
            self.artefact_segments.left.volume() - self.diagnostic_hemisphere_volume
        )
        # Calculating the right asymmetric volume and storing it in a variable.
        self.right_asymmetric_volume: float = (
            self.artefact_segments.right.volume() - self.diagnostic_hemisphere_volume
        )
        # Calculating the bilateral asymmetric volume and storing it in a
        # variable.
        self.bilateral_asymmetric_volume: float = (
            self.left_asymmetric_volume - self.right_asymmetric_volume
        )
        # Calculating the bifacial asymmetric volume and storing it in a
        # variable.
        self.bifacial_asymmetric_volume: float = (
            self.ventral_asymmetric_volume - self.dorsal_asymmetric_volume
        )

        # QUADRANT APPROACH

        # Calculating the volume of a single reference mesh quadrant and storing
        # it in a variable.
        self.reference_mesh_quadrant_volume: float = self.reference_mesh_volume / 4

        # Checking if the constructed mesh volume is less (i.e., an Endo_Sym)
        # than the total artefact segments volume.
        if self.reference_mesh_volume < self.artefact_segments.volume:
            # EQUATIONS FOR AN ENDO-SYM ANALYSIS

            # Calculating the omega coefficient of global radial symmetry
            # referencing the Y-axis and storing it in a variable.

            self.radial_symmetry: float = (
                self.reference_mesh_volume / self.artefact_segments.volume
            )

            # Calculating the QII dorsal-right asymmetric volume and storing it
            # in a variable.
            self.dorsal_right_asymmetric_volume: float = (
                self.artefact_segments.dorsal_right.volume()
                - self.reference_mesh_quadrant_volume
            )

            # Calculating the QIII dorsal-left asymmetric volume and storing it
            # in a variable.
            self.dorsal_left_asymmetric_volume: float = (
                self.artefact_segments.dorsal_left.volume()
                - self.reference_mesh_quadrant_volume
            )

            # Calculating the QI ventral-right asymmetric volume and storing it
            # in a variable.
            self.ventral_right_asymmetric_volume: float = (
                self.artefact_segments.ventral_right.volume()
                - self.reference_mesh_quadrant_volume
            )

            # Calculating the QIV ventral-left asymmetric volume and storing it
            # in a variable.
            self.ventral_left_asymmetric_volume: float = (
                self.artefact_segments.ventral_left.volume()
                - self.reference_mesh_quadrant_volume
            )

        else:
            # EQUATIONS FOR AN EXO-SYM ANALYSIS

            # If the constructed mesh volume is greater than or equal to the
            # total artefact segments volume (i.e., an Exo-Sym mesh).
            self.radial_symmetry: float = (
                self.artefact_segments.volume / self.reference_mesh_volume
            )

            # Calculating the QII dorsal-right asymmetric volume and storing it
            # in a variable.
            self.dorsal_right_asymmetric_volume: float = (
                self.reference_mesh_quadrant_volume
                - self.artefact_segments.dorsal_right.volume()
            )
            # Calculating the QIII dorsal-left asymmetric volume and storing it
            # in a variable.
            self.dorsal_left_asymmetric_volume: float = (
                self.reference_mesh_quadrant_volume
                - self.artefact_segments.dorsal_left.volume()
            )
            # Calculating the QI ventral-right asymmetric volume and storing it
            # in a variable.
            self.ventral_right_asymmetric_volume: float = (
                self.reference_mesh_quadrant_volume
                - self.artefact_segments.ventral_right.volume()
            )
            # Calculating the QIV ventral-left asymmetric volume and storing it
            # in a variable.
            self.ventral_left_asymmetric_volume: float = (
                self.reference_mesh_quadrant_volume
                - self.artefact_segments.ventral_left.volume()
            )

        # Calculating the absolute difference between QI ventral-right and QIV
        # ventral-left asymmetric volumes and storing it in a variable.
        self.bilateral_ventral_asymmetric_volume_difference: float = abs(
            self.ventral_right_asymmetric_volume - self.ventral_left_asymmetric_volume
        )
        # Calculating the absolute difference between QII dorsal-right and QIII
        # dorsal-left asymmetric volumes and storing it in a variable.
        self.bilateral_dorsal_asymmetric_volume_difference: float = abs(
            self.dorsal_right_asymmetric_volume - self.dorsal_left_asymmetric_volume
        )
        # Calculating the absolute difference between QIII dorsal-left and QIV
        # ventral-left asymmetric volumes and storing it in a variable.
        self.bifacial_left_asymmetric_volume_difference: float = abs(
            self.dorsal_left_asymmetric_volume - self.ventral_left_asymmetric_volume
        )
        # Calculating the absolute difference between QII dorsal-right and QI
        # ventral-right asymmetric volumes and storing it in a variable.
        self.bifacial_right_asymmetric_volume_difference: float = abs(
            self.dorsal_right_asymmetric_volume - self.ventral_right_asymmetric_volume
        )
        # Calculating the bilateral ventral asymmetry coefficient using a custom
        # function and storing it in a variable.
        self.bilateral_ventral_asymmetry_coefficient: float = (
            calculate_asymmetry_coefficient_of(
                vol_1=self.ventral_left_asymmetric_volume,
                vol_2=self.ventral_right_asymmetric_volume,
            )
        )
        # Calculating the bilateral dorsal asymmetry coefficient using a custom
        # function and storing it in a variable.
        self.bilateral_dorsal_asymmetry_coefficient: float = (
            calculate_asymmetry_coefficient_of(
                vol_1=self.dorsal_left_asymmetric_volume,
                vol_2=self.dorsal_right_asymmetric_volume,
            )
        )
        # Calculating the bifacial left asymmetry coefficient using a custom
        # function and storing it in a variable.
        self.bifacial_left_asymmetry_coefficient: float = (
            calculate_asymmetry_coefficient_of(
                vol_1=self.dorsal_left_asymmetric_volume,
                vol_2=self.ventral_left_asymmetric_volume,
            )
        )
        # Calculating the bifacial right asymmetry coefficient using a custom
        # function and storing it in a variable.
        self.bifacial_right_asymmetry_coefficient: float = (
            calculate_asymmetry_coefficient_of(
                vol_1=self.dorsal_right_asymmetric_volume,
                vol_2=self.ventral_right_asymmetric_volume,
            )
        )
        # Creating a bilateral MirrorSymmetry object with bilateral ventral
        # asymmetry coefficient and bilateral dorsal asymmetry coefficient.
        self.bilateral_mirror_symmetry: MirrorSymmetry = MirrorSymmetry(
            asymmetry_coefficient_1=self.bilateral_ventral_asymmetry_coefficient,
            asymmetry_coefficient_2=self.bilateral_dorsal_asymmetry_coefficient,
        )
        # Creating a bifacial MirrorSymmetry object with bifacial left asymmetry
        # coefficient and bifacial right asymmetry coefficient.
        self.bifacial_mirror_symmetry: MirrorSymmetry = MirrorSymmetry(
            asymmetry_coefficient_1=self.bifacial_left_asymmetry_coefficient,
            asymmetry_coefficient_2=self.bifacial_right_asymmetry_coefficient,
        )
        # VOLUMETRIC REFINEMENT: Calculating the volumetric refinement ratio by
        # dividing artefact volume by surface area and storing it in a variable.
        # self.refinement_volumetric: float = self.artefact_segments.volume / self.artefact_data.oriented_artefact.area() area

        # LINEAR REFINEMENT: Defining variables for minimum and maximum breadth,
        # length, and thickness values.

        self.breadth_min: float  # Minimum breadth value
        self.breadth_max: float  # Maximum breadth value
        self.length_min: float  # Minimum length value
        self.length_max: float  # Maximum length value
        self.thickness_min: float  # Minimum thickness value
        self.thickness_max: float  # Maximum thickness value

        # Extracting minimum and maximum values for breadth, length, and
        # thickness from artefact bounds.
        (
            self.breadth_min,
            self.breadth_max,
            self.length_min,
            self.length_max,
            self.thickness_min,
            self.thickness_max,
        ) = self.artefact_segments.artefact.bounds()

        # Calculating the absolute difference between maximum and minimum
        # breadth values and storing it in a variable.
        breadth: float = abs((self.breadth_max - self.breadth_min))
        # length = abs((length_max - length_min)) Calculating the absolute
        # difference between maximum and minimum thickness values and storing it
        # in a variable.
        thickness: float = abs((self.thickness_max - self.thickness_min))

        # Calculating the linear refinement ratio by dividing thickness by breadth and
        # storing it in a variable.
        self.refinement_linear: float = thickness / breadth

    def to_csv_data_dict(self):
        """
        This method constructs and returns a dictionary where each key-value
        pair represents a specific metric related to an object for exporting or
        analyzing an artefact's geometric, symmetry, and asymmetry properties.
        Each line inside the method's return statement creates a key-value pair
        in the dictionary, where the key is a string describing the data, and
        the value is formatted based on the object's attributes.
        """
        return {
            # This line calculates the reference volume of the mesh and
            # multiplies it by a scaling factor defined by Scale.VOLUME. The
            # result is formatted as a string with four decimal places. This
            # represents the total volume of the reference mesh.
            "Ref_Volume(mm^3)": f"{self.reference_mesh_volume * Scale.VOLUME:0.4f}",
            # This line calculates the volume of a quadrant (1/4) of the
            # reference mesh to a string with four decimal places for more
            # detailed analysis.
            "Ref_Quad_Volume(mm^3)": f"{self.reference_mesh_quadrant_volume:0.4f}",
            # This outputs the omega coefficient of symmetry of the object as a
            # string with four decimal places as a measure of the overall radial
            # symmetry (in reference to the Y-axis) of the artefact.
            "Radial_Symmetry": f"{self.radial_symmetry:0.4f}",
            # This outputs the arithmetic mean of the bilateral mirror symmetry
            # (BLMS) as a string, formatted to four decimal places.
            "Mean_BLMS": f"{self.bilateral_mirror_symmetry.arithmetic_mean:0.4f}",
            # This outputs the coefficient of ventral bilateral asymmetry,
            # converting it into a string with four decimal places. This value
            # represents the asymmetry on the ventral face of the artefact.
            "Ventral_BLMS": f"{self.bilateral_ventral_asymmetry_coefficient:0.4f}",
            # This outputs the coefficient of dorsal bilateral asymmetry,
            # converting it into a string with four decimal places. This value
            # represents the asymmetry on the dorsal face of the artefact.
            "Dorsal_BLMS": f"{self.bilateral_dorsal_asymmetry_coefficient:0.4f}",
            # This outputs the arithmetic mean of the bifacial mirror symmetry
            # (BFMS) as a string, formatted to four decimal places.
            "Mean_BFMS": f"{self.bifacial_mirror_symmetry.arithmetic_mean:0.4f}",
            # This outputs the coefficient of left-hand bifacial asymmetry,
            # converting it into a string with four decimal places. This value
            # represents the asymmetry on the left-hand side of the artefact.
            "Left_BFMS": f"{self.bifacial_left_asymmetry_coefficient:0.4f}",
            # This outputs the coefficient of right-hand bifacial asymmetry,
            # converting it into a string with four decimal places. This value
            # represents the asymmetry on the right-hand side of the artefact.
            "Right_BFMS": f"{self.bifacial_right_asymmetry_coefficient:0.4f}",
            # This line multiplies a refinement ratio by a scaling factor
            # defined by Scale.LENGTH, formatting the result to four decimal
            # places as a string, representing the thinness or 'refinement' of
            # the artefact.
            # "Volumetric_Refinement": f"{self.refinement_volumetric * Scale.VOLUME:0.4f}",
            # This line multiplies a volumetric refinement ratio by a scaling factor
            # defined by Scale.VOLUME, formatting the result to four decimal
            # places as a string, representing the thinness or 'refinement' of
            # the artefact.
            "Linear_Refinement": f"{self.refinement_linear * Scale.LENGTH:0.4f}",
            # This converts the artefact's ventral-right asymmetric volume to a
            # string without specifying a format. It represents the asymmetric
            # volume of QI or the ventral-right quadrant of the artefact.
            "Ventral_Right_Asym_Volume(mm^3)": f"{self.ventral_right_asymmetric_volume:.4f}",
            # This converts the artefact's dorsal-right asymmetric volume to a
            # string without specifying a format. It represents the asymmetric
            # volume of QII or the dorsal-right quadrant of the artefact.
            "Dorsal_Right_Asym_Volume(mm^3)": f"{self.dorsal_right_asymmetric_volume:.4f}",
            # This converts the artefact's dorsal-left asymmetric volume to a
            # string without specifying a format. It represents the asymmetric
            # volume of QIII or the dorsal-left quadrant of the artefact.
            "Dorsal_Left_Asym_Volume(mm^3)": f"{self.dorsal_left_asymmetric_volume:.4f}",
            # This converts the artefact's ventral-left asymmetric volume to a
            # string without specifying a format. It represents the asymmetric
            # volume of QIV or the ventral-left quadrant of the artefact.
            "Ventral_Left_Asym_Volume(mm^3)": f"{self.ventral_left_asymmetric_volume:.4f}",
        }

    def to_volume_data_dict(self):
        return {
            "Artefact_Volume": self.artefact_segments.volume * Scale.VOLUME,
            "Length_Max": self.length_max * Scale.LENGTH,
            "Length_Min": self.length_min * Scale.LENGTH,
            "Thickness_Max": self.thickness_max * Scale.LENGTH,
            "Thickness_Min": self.thickness_min * Scale.LENGTH,
            "Breadth_Max": self.breadth_max * Scale.LENGTH,
            "Breadth_Min": self.breadth_max * Scale.LENGTH,
            "Volume_QI": self.artefact_segments.ventral_right.volume() * Scale.VOLUME,
            "Volume_QII": self.artefact_segments.dorsal_right.volume() * Scale.VOLUME,
            "Volume_QIII": self.artefact_segments.dorsal_left.volume() * Scale.VOLUME,
            "Volume_QIV": self.artefact_segments.ventral_left.volume() * Scale.VOLUME,
        }
