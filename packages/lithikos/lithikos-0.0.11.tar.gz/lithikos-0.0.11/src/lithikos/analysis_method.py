"""Implementation of AnalysisMethod"""

from enum import Enum

from . import ArtefactUtilsParseException


class AnalysisMethod(Enum):
    """Enum defining the anaysis methods supported with associated meta data"""

    ENDO_SYM = ("Endo-Sym", "endo-sym", "magenta")
    MEAN_SYM = ("Mean-Sym", "mean-sym", "red")
    EXO_SYM = ("Exo-Sym", "exo-sym", "blue")

    def __init__(self, text, abbreviation, colour):
        self.text = text
        self.abbreviation = abbreviation
        self.colour = colour

    @staticmethod
    def from_text(text: str):
        """Method to set AnalysisMethod based on text matching associated meta data"""
        for analysis_method in AnalysisMethod:
            if text == analysis_method.text:
                return analysis_method
        # No matching orientation method found
        raise (
            ArtefactUtilsParseException(
                f"Unable to create AnalysisMethod from text: {text}."
            )
        )
