from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.abgabe_art import AbgabeArt
from ..enum.energierichtung import Energierichtung
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.waermenutzung import Waermenutzung

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .konzessionsabgabe import Konzessionsabgabe
    from .verwendungszweck_pro_marktrolle import VerwendungszweckProMarktrolle
    from .zaehlzeitregister import Zaehlzeitregister


class Zaehlwerk(BaseModel):
    """
    Mit dieser Komponente werden Zählwerke modelliert.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zaehlwerk.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zaehlwerk JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Zaehlwerk.json>`_
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
    anzahl_ablesungen: Optional[int] = Field(default=None, alias="anzahlAblesungen", title="Anzahlablesungen")
    """
    Abrechnungsrelevant
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    einheit: Optional[Mengeneinheit] = None
    ist_abrechnungsrelevant: Optional[bool] = Field(
        default=None, alias="istAbrechnungsrelevant", title="Istabrechnungsrelevant"
    )
    """
    Anzahl der Nachkommastellen
    """
    ist_schwachlastfaehig: Optional[bool] = Field(
        default=None, alias="istSchwachlastfaehig", title="Istschwachlastfaehig"
    )
    """
    Schwachlastfaehigkeit
    """
    ist_steuerbefreit: Optional[bool] = Field(default=None, alias="istSteuerbefreit", title="Iststeuerbefreit")
    """
    Konzessionsabgabe
    """
    ist_unterbrechbar: Optional[bool] = Field(default=None, alias="istUnterbrechbar", title="Istunterbrechbar")
    """
    Stromverbrauchsart/Verbrauchsart Marktlokation
    """
    konzessionsabgabe: Optional["Konzessionsabgabe"] = None
    """
    Wärmenutzung Marktlokation
    """
    nachkommastelle: Optional[int] = Field(default=None, title="Nachkommastelle")
    """
    Anzahl der Vorkommastellen
    """
    obis_kennzahl: str = Field(..., alias="obisKennzahl", title="Obiskennzahl")
    richtung: Optional[Energierichtung] = None
    verbrauchsart: Optional[str] = Field(default=None, title="Verbrauchsart")
    verwendungszwecke: Optional[list["VerwendungszweckProMarktrolle"]] = Field(default=None, title="Verwendungszwecke")
    """
    Schwachlastfaehigkeit
    """
    vorkommastelle: Optional[int] = Field(default=None, title="Vorkommastelle")
    """
    Steuerbefreiung
    """
    waermenutzung: Optional[Waermenutzung] = None
    """
    Unterbrechbarkeit Marktlokation
    """
    wandlerfaktor: Optional[Decimal] = Field(default=None, title="Wandlerfaktor")
    zaehlwerk_id: Optional[str] = Field(default=None, alias="zaehlwerkId", title="Zaehlwerkid")
    zaehlzeitregister: Optional["Zaehlzeitregister"] = None
    """
    Anzahl Ablesungen pro Jahr
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    vorkommastellen: int = Field(..., title="Vorkommastellen")
    nachkommastellen: int = Field(..., title="Nachkommastellen")
    schwachlastfaehig: bool = Field(..., title="Schwachlastfaehig")
    konzessionsabgaben_typ: Optional[AbgabeArt] = Field(default=None, alias="konzessionsabgabenTyp")
    active_from: datetime = Field(..., alias="activeFrom", title="Activefrom")
    active_until: Optional[datetime] = Field(default=None, alias="activeUntil", title="Activeuntil")
    description: Optional[str] = Field(default=None, title="Description")
