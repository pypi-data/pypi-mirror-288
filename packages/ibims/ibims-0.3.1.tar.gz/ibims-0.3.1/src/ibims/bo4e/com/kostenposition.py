from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .betrag import Betrag
    from .menge import Menge
    from .preis import Preis


class Kostenposition(BaseModel):
    """
    Diese Komponente wird zur Übertagung der Details zu einer Kostenposition verwendet.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Kostenposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Kostenposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Kostenposition.json>`_
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
    artikelbezeichnung: Optional[str] = Field(default=None, title="Artikelbezeichnung")
    """
    Bezeichnung für den Artikel für den die Kosten ermittelt wurden. Beispiel: Arbeitspreis HT
    """
    artikeldetail: Optional[str] = Field(default=None, title="Artikeldetail")
    """
    Detaillierung des Artikels (optional). Beispiel: 'Drehstromzähler'
    """
    betrag_kostenposition: Optional["Betrag"] = Field(default=None, alias="betragKostenposition")
    """
    Der errechnete Gesamtbetrag der Position als Ergebnis der Berechnung <Menge * Einzelpreis> oder
    <Einzelpreis / (Anzahl Tage Jahr) * zeitmenge>
    """
    bis: Optional[datetime] = Field(default=None, title="Bis")
    """
    exklusiver bis-Zeitpunkt der Kostenzeitscheibe
    """
    einzelpreis: Optional["Preis"] = None
    """
    Der Preis für eine Einheit. Beispiele: 5,8200 ct/kWh oder 55 €/Jahr.
    """
    menge: Optional["Menge"] = None
    """
    Die Menge, die in die Kostenberechnung eingeflossen ist. Beispiel: 3.660 kWh
    """
    positionstitel: Optional[str] = Field(default=None, title="Positionstitel")
    """
    Ein Titel für die Zeile. Hier kann z.B. der Netzbetreiber eingetragen werden, wenn es sich um Netzkosten handelt.
    """
    von: Optional[datetime] = Field(default=None, title="Von")
    """
    inklusiver von-Zeitpunkt der Kostenzeitscheibe
    """
    zeitmenge: Optional["Menge"] = None
    """
    Wenn es einen zeitbasierten Preis gibt (z.B. €/Jahr), dann ist hier die Menge angegeben mit der die Kosten berechnet
    wurden. Z.B. 138 Tage.
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
