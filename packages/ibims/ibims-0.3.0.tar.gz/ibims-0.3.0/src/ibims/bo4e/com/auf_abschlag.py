from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.auf_abschlagstyp import AufAbschlagstyp
from ..enum.auf_abschlagsziel import AufAbschlagsziel
from ..enum.waehrungseinheit import Waehrungseinheit

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .preisstaffel import Preisstaffel
    from .zeitraum import Zeitraum


class AufAbschlag(BaseModel):
    """
    Modell für die preiserhöhenden (Aufschlag) bzw. preisvermindernden (Abschlag) Zusatzvereinbarungen,
    die individuell zu einem neuen oder bestehenden Liefervertrag abgeschlossen wurden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/AufAbschlag.svg" type="image/svg+xml"></object>

    .. HINT::
        `AufAbschlag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/AufAbschlag.json>`_
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
    Typ des Aufabschlages (z.B. absolut oder prozentual).
    """
    auf_abschlagsziel: Optional[AufAbschlagsziel] = Field(default=None, alias="aufAbschlagsziel")
    """
    Diesem Preis oder den Kosten ist der Auf/Abschlag zugeordnet. Z.B. Arbeitspreis, Gesamtpreis etc..
    """
    beschreibung: Optional[str] = Field(default=None, title="Beschreibung")
    """
    Beschreibung zum Auf-/Abschlag
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    """
    Bezeichnung des Auf-/Abschlags
    """
    einheit: Optional[Waehrungseinheit] = None
    """
    Gibt an in welcher Währungseinheit der Auf/Abschlag berechnet wird. Euro oder Ct..
    (Nur im Falle absoluter Aufschlagstypen).
    """
    gueltigkeitszeitraum: Optional["Zeitraum"] = None
    """
    Internetseite, auf der die Informationen zum Auf-/Abschlag veröffentlicht sind.
    """
    staffeln: Optional[list["Preisstaffel"]] = Field(default=None, title="Staffeln")
    """
    Werte für die gestaffelten Auf/Abschläge.
    """
    website: Optional[str] = Field(default=None, title="Website")
    """
    Internetseite, auf der die Informationen zum Auf-/Abschlag veröffentlicht sind.
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
