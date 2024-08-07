from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.lokationstyp import Lokationstyp
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.verbrauch import Verbrauch
    from ..zusatz_attribut import ZusatzAttribut


class Energiemenge(BaseModel):
    """
    Abbildung von Mengen, die Lokationen zugeordnet sind

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Energiemenge.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energiemenge JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Energiemenge.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.ENERGIEMENGE, alias="_typ")
    """
    Eindeutige Nummer der Marktlokation bzw. der Messlokation, zu der die Energiemenge gehört
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    energieverbrauch: list["Verbrauch"] = Field(..., title="Energieverbrauch")
    """
    Gibt den Verbrauch in einer Zeiteinheit an
    """
    lokations_id: Optional[str] = Field(default=None, alias="lokationsId", title="Lokationsid")
    """
    Eindeutige Nummer der Marktlokation bzw. der Messlokation, zu der die Energiemenge gehört
    """
    lokationstyp: Optional[Lokationstyp] = None
    """
    Gibt an, ob es sich um eine Markt- oder Messlokation handelt
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
