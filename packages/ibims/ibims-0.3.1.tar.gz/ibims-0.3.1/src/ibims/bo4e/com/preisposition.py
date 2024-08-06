from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.bdew_artikelnummer import BDEWArtikelnummer
from ..enum.bemessungsgroesse import Bemessungsgroesse
from ..enum.kalkulationsmethode import Kalkulationsmethode
from ..enum.leistungstyp import Leistungstyp
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.steuerkennzeichen import Steuerkennzeichen
from ..enum.tarifzeit import Tarifzeit
from ..enum.waehrungseinheit import Waehrungseinheit

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .preisstaffel import Preisstaffel


class Preisposition(BaseModel):
    """
    Preis für eine definierte Lieferung oder Leistung innerhalb eines Preisblattes

    .. raw:: html

        <object data="../_static/images/bo4e/com/Preisposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Preisposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Preisposition.json>`_
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
    bdew_artikelnummer: Optional[BDEWArtikelnummer] = Field(default=None, alias="bdewArtikelnummer")
    """
    Eine vom BDEW standardisierte Bezeichnug für die abgerechnete Leistungserbringung;
    Diese Artikelnummer wird auch im Rechnungsteil der INVOIC verwendet.
    """
    berechnungsmethode: Optional[Kalkulationsmethode] = None
    """
    Das Modell, das der Preisbildung zugrunde liegt
    """
    bezugsgroesse: Optional[Mengeneinheit] = None
    """
    Hier wird festgelegt, auf welche Bezugsgrösse sich der Preis bezieht, z.B. kWh oder Stück
    """
    freimenge_blindarbeit: Optional[Decimal] = Field(
        default=None, alias="freimengeBlindarbeit", title="Freimengeblindarbeit"
    )
    """
    Der Anteil der Menge der Blindarbeit in Prozent von der Wirkarbeit, für die keine Abrechnung erfolgt
    """
    freimenge_leistungsfaktor: Optional[Decimal] = Field(
        default=None, alias="freimengeLeistungsfaktor", title="Freimengeleistungsfaktor"
    )
    """
    Der cos phi (Verhältnis Wirkleistung/Scheinleistung) aus dem die Freimenge für die Blindarbeit berechnet wird als
    tan phi (Verhältnis Blindleistung/Wirkleistung)
    """
    gruppenartikel_id: Optional[str] = Field(default=None, alias="gruppenartikelId", title="Gruppenartikelid")
    """
    Übergeordnete Gruppen-ID, die sich ggf. auf die Artikel-ID in der Preisstaffel bezieht
    """
    leistungsbezeichnung: Optional[str] = Field(default=None, title="Leistungsbezeichnung")
    """
    Bezeichnung für die in der Position abgebildete Leistungserbringung
    """
    leistungstyp: Optional[Leistungstyp] = None
    """
    Standardisierte Bezeichnung für die abgerechnete Leistungserbringung
    """
    preiseinheit: Optional[Waehrungseinheit] = None
    """
    Festlegung, mit welcher Preiseinheit abgerechnet wird, z.B. Ct. oder €
    """
    preisstaffeln: list["Preisstaffel"] = Field(..., title="Preisstaffeln")
    """
    Preisstaffeln, die zu dieser Preisposition gehören
    """
    tarifzeit: Optional[Tarifzeit] = None
    """
    Festlegung, für welche Tarifzeit der Preis hier festgelegt ist
    """
    zeitbasis: Optional[Mengeneinheit] = None
    """
    Die Zeit(dauer) auf die sich der Preis bezieht.
    Z.B. ein Jahr für einen Leistungspreis der in €/kW/Jahr ausgegeben wird
    """
    zonungsgroesse: Optional[Bemessungsgroesse] = None
    """
    Mit der Menge der hier angegebenen Größe wird die Staffelung/Zonung durchgeführt. Z.B. Vollbenutzungsstunden
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    steuersatz: Steuerkennzeichen
