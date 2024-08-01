from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.preisgarantietyp import Preisgarantietyp

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .zeitraum import Zeitraum


class Preisgarantie(BaseModel):
    """
    Definition für eine Preisgarantie mit der Möglichkeit verschiedener Ausprägungen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Preisgarantie.svg" type="image/svg+xml"></object>

    .. HINT::
        `Preisgarantie JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Preisgarantie.json>`_
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
    beschreibung: Optional[str] = Field(default=None, title="Beschreibung")
    """
    Freitext zur Beschreibung der Preisgarantie.
    """
    preisgarantietyp: Optional[Preisgarantietyp] = None
    """
    Festlegung, auf welche Preisbestandteile die Garantie gewährt wird.
    """
    zeitliche_gueltigkeit: "Zeitraum" = Field(..., alias="zeitlicheGueltigkeit")
    """
    Zeitraum, bis zu dem die Preisgarantie gilt, z.B. bis zu einem absolutem / fixem Datum
    oder als Laufzeit in Monaten.
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    creation_date: Optional[datetime] = Field(default=None, alias="creationDate", title="Creationdate")
