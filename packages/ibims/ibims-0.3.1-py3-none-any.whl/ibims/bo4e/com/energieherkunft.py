from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.erzeugungsart import Erzeugungsart

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Energieherkunft(BaseModel):
    """
    Abbildung einer Energieherkunft

    .. raw:: html

        <object data="../_static/images/bo4e/com/Energieherkunft.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energieherkunft JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Energieherkunft.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Eine generische ID, die für eigene Zwecke genutzt werden kann.
    Z.B. könnten hier UUIDs aus einer Datenbank stehen oder URLs zu einem Backend-System.
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    anteil_prozent: Optional[Decimal] = Field(default=None, alias="anteilProzent", title="Anteilprozent")
    """
    Prozentualer Anteil der jeweiligen Erzeugungsart.
    """
    erzeugungsart: Optional[Erzeugungsart] = None
    """
    Art der Erzeugung der Energie.
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
