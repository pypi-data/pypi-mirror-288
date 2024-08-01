from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.messwertstatus import Messwertstatus
from ..enum.messwertstatuszusatz import Messwertstatuszusatz

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .zeitspanne import Zeitspanne


class Zeitreihenwert(BaseModel):
    """
    Abbildung eines Zeitreihenwertes bestehend aus Zeitraum, Wert und Statusinformationen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zeitreihenwert.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitreihenwert JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Zeitreihenwert.json>`_
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
    status: Optional[Messwertstatus] = None
    """
    Der Status gibt an, wie der Wert zu interpretieren ist, z.B. in Berechnungen.
    """
    statuszusatz: Optional[Messwertstatuszusatz] = None
    """
    Eine Zusatzinformation zum Status, beispielsweise ein Grund für einen fehlenden Wert.
    """
    wert: Optional[Decimal] = Field(default=None, title="Wert")
    """
    Zeitespanne für das Messintervall
    """
    zeitspanne: Optional["Zeitspanne"] = None
    """
    Zeitespanne für das Messintervall
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
