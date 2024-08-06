from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.kundentyp import Kundentyp
from ..enum.registeranzahl import Registeranzahl
from ..enum.sparte import Sparte
from ..enum.tarifmerkmal import Tarifmerkmal
from ..enum.tariftyp import Tariftyp
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.auf_abschlag import AufAbschlag
    from ..com.energiemix import Energiemix
    from ..com.preisgarantie import Preisgarantie
    from ..com.tarifberechnungsparameter import Tarifberechnungsparameter
    from ..com.tarifeinschraenkung import Tarifeinschraenkung
    from ..com.tarifpreisposition import Tarifpreisposition
    from ..com.vertragskonditionen import Vertragskonditionen
    from ..com.zeitraum import Zeitraum
    from ..zusatz_attribut import ZusatzAttribut
    from .marktteilnehmer import Marktteilnehmer


class Tarifpreisblatt(BaseModel):
    """
    Tarifinformation mit Preisen, Aufschlägen und Berechnungssystematik

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Tarifpreisblatt.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifpreisblatt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Tarifpreisblatt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.TARIFPREISBLATT, alias="_typ")
    """
    Gibt an, wann der Preis zuletzt angepasst wurde
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    anbieter: Optional["Marktteilnehmer"] = None
    """
    Der Marktteilnehmer (Lieferant), der diesen Tarif anbietet
    """
    anbietername: Optional[str] = Field(default=None, title="Anbietername")
    """
    Der Name des Marktpartners, der den Tarif anbietet
    """
    anwendung_von: Optional[datetime] = Field(default=None, alias="anwendungVon", title="Anwendungvon")
    bemerkung: Optional[str] = Field(default=None, title="Bemerkung")
    """
    Freitext
    """
    berechnungsparameter: Optional["Tarifberechnungsparameter"] = None
    """
    Für die Berechnung der Kosten sind die hier abgebildeten Parameter heranzuziehen
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    """
    Name des Tarifs
    """
    energiemix: Optional["Energiemix"] = None
    """
    Der Energiemix, der für diesen Tarif gilt
    """
    kundentypen: Optional[list[Kundentyp]] = Field(default=None, title="Kundentypen")
    """
    Kundentypen für den der Tarif gilt, z.B. Privatkunden
    """
    preisgarantie: Optional["Preisgarantie"] = None
    """
    Festlegung von Garantien für bestimmte Preisanteile
    """
    preisstand: Optional[datetime] = Field(default=None, title="Preisstand")
    """
    Gibt an, wann der Preis zuletzt angepasst wurde
    """
    registeranzahl: Optional[Registeranzahl] = None
    """
    Die Art des Tarifes, z.B. Eintarif oder Mehrtarif
    """
    sparte: Optional[Sparte] = None
    """
    Strom oder Gas, etc.
    """
    tarif_auf_abschlaege: Optional[list["AufAbschlag"]] = Field(
        default=None, alias="tarifAufAbschlaege", title="Tarifaufabschlaege"
    )
    """
    Auf- und Abschläge auf die Preise oder Kosten
    """
    tarifeinschraenkung: Optional["Tarifeinschraenkung"] = None
    """
    Die Bedingungen und Einschränkungen unter denen ein Tarif angewendet werden kann
    """
    tarifmerkmale: Optional[list[Tarifmerkmal]] = Field(default=None, title="Tarifmerkmale")
    """
    Weitere Merkmale des Tarifs, z.B. Festpreis oder Vorkasse
    """
    tarifpreise: Optional[list["Tarifpreisposition"]] = Field(default=None, title="Tarifpreise")
    """
    Die festgelegten Preise, z.B. für Arbeitspreis, Grundpreis etc.
    """
    tariftyp: Optional[Tariftyp] = None
    """
    Hinweis auf den Tariftyp, z.B. Grundversorgung oder Sondertarif
    """
    vertragskonditionen: Optional["Vertragskonditionen"] = None
    """
    Mindestlaufzeiten und Kündigungsfristen zusammengefasst
    """
    website: Optional[str] = Field(default=None, title="Website")
    """
    Internetseite auf dem der Tarif zu finden ist
    """
    zeitliche_gueltigkeit: Optional["Zeitraum"] = Field(default=None, alias="zeitlicheGueltigkeit")
    """
    Angabe, in welchem Zeitraum der Tarif gültig ist
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
