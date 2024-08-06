from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.preismodell import Preismodell
from ..enum.rechnungslegung import Rechnungslegung
from ..enum.sparte import Sparte
from ..enum.vertragsform import Vertragsform

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .ausschreibungsdetail import Ausschreibungsdetail
    from .menge import Menge
    from .zeitraum import Zeitraum


class Ausschreibungslos(BaseModel):
    """
    Eine Komponente zur Abbildung einzelner Lose einer Ausschreibung

    .. raw:: html

        <object data="../_static/images/bo4e/com/Ausschreibungslos.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ausschreibungslos JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Ausschreibungslos.json>`_
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
    anzahl_lieferstellen: Optional[int] = Field(default=None, alias="anzahlLieferstellen", title="Anzahllieferstellen")
    """
    Anzahl der Lieferstellen in dieser Ausschreibung
    """
    bemerkung: Optional[str] = Field(default=None, title="Bemerkung")
    """
    Bemerkung des Kunden zum Los
    """
    betreut_durch: Optional[str] = Field(default=None, alias="betreutDurch", title="Betreutdurch")
    """
    Name des Lizenzpartners
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    """
    Bezeichnung der Ausschreibung
    """
    energieart: Optional[Sparte] = None
    """
    Unterscheidungsmöglichkeiten für die Sparte
    """
    gesamt_menge: Optional["Menge"] = Field(default=None, alias="gesamtMenge")
    """
    Gibt den Gesamtjahresverbrauch (z.B. in kWh) aller in diesem Los enthaltenen Lieferstellen an
    """
    lieferstellen: Optional[list["Ausschreibungsdetail"]] = Field(default=None, title="Lieferstellen")
    """
    Die ausgeschriebenen Lieferstellen
    """
    lieferzeitraum: Optional["Zeitraum"] = None
    """
    Zeitraum, für den die in diesem Los enthaltenen Lieferstellen beliefert werden sollen
    """
    losnummer: Optional[str] = Field(default=None, title="Losnummer")
    """
    Laufende Nummer des Loses
    """
    preismodell: Optional[Preismodell] = None
    """
    Bezeichnung der Preismodelle in Ausschreibungen für die Energielieferung
    """
    wiederholungsintervall: Optional["Zeitraum"] = None
    """
    In welchem Intervall die Angebotsabgabe wiederholt werden darf.
    Angabe nur gesetzt für die 2. Phase bei öffentlich-rechtlichen Ausschreibungen
    """
    wunsch_kuendingungsfrist: Optional["Zeitraum"] = Field(default=None, alias="wunschKuendingungsfrist")
    """
    Kundenwunsch zur Kündigungsfrist in der Ausschreibung
    """
    wunsch_maximalmenge: Optional["Menge"] = Field(default=None, alias="wunschMaximalmenge")
    """
    Maximalmenge Toleranzband (kWh, %)
    """
    wunsch_mindestmenge: Optional["Menge"] = Field(default=None, alias="wunschMindestmenge")
    """
    Mindesmenge Toleranzband (kWh, %)
    """
    wunsch_rechnungslegung: Optional[Rechnungslegung] = Field(default=None, alias="wunschRechnungslegung")
    """
    Aufzählung der Möglichkeiten zur Rechnungslegung in Ausschreibungen
    """
    wunsch_vertragsform: Optional[Vertragsform] = Field(default=None, alias="wunschVertragsform")
    """
    Aufzählung der Möglichkeiten zu Vertragsformen in Ausschreibungen
    """
    wunsch_zahlungsziel: Optional["Zeitraum"] = Field(default=None, alias="wunschZahlungsziel")
    """
    Kundenwunsch zum Zahlungsziel in der Ausschreibung
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
