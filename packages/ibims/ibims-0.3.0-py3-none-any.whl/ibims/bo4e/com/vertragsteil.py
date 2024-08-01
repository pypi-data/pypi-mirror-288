from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .menge import Menge


class Vertragsteil(BaseModel):
    """
    Abbildung für einen Vertragsteil. Der Vertragsteil wird dazu verwendet,
    eine vertragliche Leistung in Bezug zu einer Lokation (Markt- oder Messlokation) festzulegen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Vertragsteil.svg" type="image/svg+xml"></object>

    .. HINT::
        `Vertragsteil JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Vertragsteil.json>`_
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
    lokation: Optional[str] = Field(default=None, title="Lokation")
    """
    Der Identifier für diejenigen Markt- oder Messlokation, die zu diesem Vertragsteil gehören.
    Verträge für mehrere Lokationen werden mit mehreren Vertragsteilen abgebildet
    """
    maximale_abnahmemenge: Optional["Menge"] = Field(default=None, alias="maximaleAbnahmemenge")
    """
    Für die Lokation festgelegte maximale Abnahmemenge (exklusiv)
    """
    minimale_abnahmemenge: Optional["Menge"] = Field(default=None, alias="minimaleAbnahmemenge")
    """
    Für die Lokation festgelegte Mindestabnahmemenge (inklusiv)
    """
    vertraglich_fixierte_menge: Optional["Menge"] = Field(default=None, alias="vertraglichFixierteMenge")
    """
    Für die Lokation festgeschriebene Abnahmemenge
    """
    vertragsteilbeginn: Optional[datetime] = Field(default=None, title="Vertragsteilbeginn")
    """
    Start der Gültigkeit des Vertragsteils (inklusiv)
    """
    vertragsteilende: Optional[datetime] = Field(default=None, title="Vertragsteilende")
    """
    Ende der Gültigkeit des Vertragsteils (exklusiv)
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
