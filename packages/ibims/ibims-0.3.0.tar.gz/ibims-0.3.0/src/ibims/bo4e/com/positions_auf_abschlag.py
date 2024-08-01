from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.auf_abschlagstyp import AufAbschlagstyp
from ..enum.waehrungseinheit import Waehrungseinheit

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class PositionsAufAbschlag(BaseModel):
    """
    Differenzierung der zu betrachtenden Produkte anhand der preiserhöhenden (Aufschlag)
    bzw. preisvermindernden (Abschlag) Zusatzvereinbarungen,
    die individuell zu einem neuen oder bestehenden Liefervertrag abgeschlossen werden können.
    Es können mehrere Auf-/Abschläge gleichzeitig ausgewählt werden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/PositionsAufAbschlag.svg" type="image/svg+xml"></object>

    .. HINT::
        `PositionsAufAbschlag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/PositionsAufAbschlag.json>`_
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
    auf_abschlagstyp: Optional[AufAbschlagstyp] = Field(default=None, alias="aufAbschlagstyp")
    """
    Typ des AufAbschlages
    """
    auf_abschlagswaehrung: Optional[Waehrungseinheit] = Field(default=None, alias="aufAbschlagswaehrung")
    """
    Einheit, in der der Auf-/Abschlag angegeben ist (z.B. ct/kWh).
    """
    auf_abschlagswert: Optional[Decimal] = Field(default=None, alias="aufAbschlagswert", title="Aufabschlagswert")
    """
    Höhe des Auf-/Abschlages
    """
    beschreibung: Optional[str] = Field(default=None, title="Beschreibung")
    """
    Beschreibung zum Auf-/Abschlag
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    """
    Bezeichnung des Auf-/Abschlags
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
