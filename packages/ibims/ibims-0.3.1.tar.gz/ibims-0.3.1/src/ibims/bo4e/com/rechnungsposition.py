from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.bdew_artikelnummer import BDEWArtikelnummer
from ..enum.mengeneinheit import Mengeneinheit

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .betrag import Betrag
    from .menge import Menge
    from .preis import Preis
    from .steuerbetrag import Steuerbetrag


class Rechnungsposition(BaseModel):
    """
    Über Rechnungspositionen werden Rechnungen strukturiert.
    In einem Rechnungsteil wird jeweils eine in sich geschlossene Leistung abgerechnet.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Rechnungsposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Rechnungsposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Rechnungsposition.json>`_
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
    artikel_id: Optional[str] = Field(default=None, alias="artikelId", title="Artikelid")
    """
    Standardisierte vom BDEW herausgegebene Liste, welche im Strommarkt die BDEW-Artikelnummer ablöst
    """
    artikelnummer: Optional[BDEWArtikelnummer] = None
    """
    Kennzeichnung der Rechnungsposition mit der Standard-Artikelnummer des BDEW
    """
    einzelpreis: Optional["Preis"] = None
    """
    Der Preis für eine Einheit der energetischen Menge
    """
    lieferung_bis: Optional[datetime] = Field(default=None, alias="lieferungBis", title="Lieferungbis")
    """
    Ende der Lieferung für die abgerechnete Leistung (exklusiv)
    """
    lieferung_von: Optional[datetime] = Field(default=None, alias="lieferungVon", title="Lieferungvon")
    """
    Start der Lieferung für die abgerechnete Leistung (inklusiv)
    """
    lokations_id: Optional[str] = Field(default=None, alias="lokationsId", title="Lokationsid")
    """
    Marktlokation, die zu dieser Position gehört
    """
    positions_menge: "Menge" = Field(..., alias="positionsMenge")
    """
    Die abgerechnete Menge mit Einheit
    """
    positionsnummer: Optional[int] = Field(default=None, title="Positionsnummer")
    """
    Fortlaufende Nummer für die Rechnungsposition
    """
    positionstext: Optional[str] = Field(default=None, title="Positionstext")
    """
    Bezeichung für die abgerechnete Position
    """
    teilrabatt_netto: Optional["Betrag"] = Field(default=None, alias="teilrabattNetto")
    """
    Nettobetrag für den Rabatt dieser Position
    """
    teilsumme_netto: "Betrag" = Field(..., alias="teilsummeNetto")
    """
    Das Ergebnis der Multiplikation aus einzelpreis * positionsMenge * (Faktor aus zeitbezogeneMenge).
    Z.B. 12,60€ * 120 kW * 3/12 (für 3 Monate).
    """
    teilsumme_steuer: "Steuerbetrag" = Field(..., alias="teilsummeSteuer")
    """
    Auf die Position entfallende Steuer, bestehend aus Steuersatz und Betrag
    """
    zeitbezogene_menge: Optional["Menge"] = Field(default=None, alias="zeitbezogeneMenge")
    """
    Eine auf die Zeiteinheit bezogene Untermenge.
    Z.B. bei einem Jahrespreis, 3 Monate oder 146 Tage.
    Basierend darauf wird der Preis aufgeteilt.
    """
    zeiteinheit: Optional[Mengeneinheit] = None
    """
    Falls sich der Preis auf eine Zeit bezieht, steht hier die Einheit
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
