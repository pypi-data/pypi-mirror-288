from enum import Enum


class EMobilitaetsart(str, Enum):
    """
    Art der E-Mobilität
    """

    WALLBOX = "WALLBOX"
    E_MOBILITAETSLADESAEULE = "E_MOBILITAETSLADESAEULE"
    LADEPARK = "LADEPARK"
