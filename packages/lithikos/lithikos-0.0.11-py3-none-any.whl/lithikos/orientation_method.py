from . import ArtefactUtilsParseException

from enum import Enum


class OrientationMethod(Enum):
    ORIENT_TIP_TO_BUTT = ("Tip2Butt", "T2B", "Tip to Butt")
    ORIENT_TIP_TO_COM = ("Tip2CoM", "T2C", "Tip to Centre of Mass")
    ORIENT_TIP_TO_COHM = ("Tip2CoHM", "T2H", "Tip to Centre of Hollow Mesh")
    ORIENT_TO_FITLINE = ("FitLine", "FIT", "Fit line through points")

    def __init__(
        self,
        text,
        abbreviation,
        description,
    ):
        self.text = text
        self.abbreviation = abbreviation
        self.description = description

    @staticmethod
    def from_text(text):
        for orientation_method in OrientationMethod:
            if text == orientation_method.text:
                return orientation_method
        # No matching orientation method found
        raise (
            ArtefactUtilsParseException(
                f"Unable to create OrintationMethod from text: {text}."
            )
        )
