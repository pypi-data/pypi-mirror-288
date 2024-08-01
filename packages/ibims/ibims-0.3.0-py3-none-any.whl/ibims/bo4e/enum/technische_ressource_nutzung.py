from enum import Enum


class TechnischeRessourceNutzung(str, Enum):
    """
    Nutzung der technischen Ressource
    """

    STROMVERBRAUCHSART = "STROMVERBRAUCHSART"
    STROMERZEUGUNGSART = "STROMERZEUGUNGSART"
    SPEICHER = "SPEICHER"
