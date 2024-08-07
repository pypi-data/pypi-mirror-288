from enum import Enum


class TechnischeRessourceVerbrauchsart(str, Enum):
    """
    Verbrauchsart der technischen Ressource
    """

    KRAFT_LICHT = "KRAFT_LICHT"
    WAERME = "WAERME"
    E_MOBILITAET = "E_MOBILITAET"
    STRASSENBELEUCHTUNG = "STRASSENBELEUCHTUNG"
