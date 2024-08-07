from enum import Enum


class SteuerkanalLeistungsbeschreibung(str, Enum):
    """
    Beschreibung des Steuerkanals
    """

    AN_AUS = "AN_AUS"
    GESTUFT = "GESTUFT"
