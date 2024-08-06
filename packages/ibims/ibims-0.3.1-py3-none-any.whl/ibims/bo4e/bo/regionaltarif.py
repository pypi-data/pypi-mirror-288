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
    from ..com.energiemix import Energiemix
    from ..com.regionale_preisgarantie import RegionalePreisgarantie
    from ..com.regionale_tarifpreisposition import RegionaleTarifpreisposition
    from ..com.regionaler_auf_abschlag import RegionalerAufAbschlag
    from ..com.tarifberechnungsparameter import Tarifberechnungsparameter
    from ..com.tarifeinschraenkung import Tarifeinschraenkung
    from ..com.vertragskonditionen import Vertragskonditionen
    from ..com.zeitraum import Zeitraum
    from ..zusatz_attribut import ZusatzAttribut
    from .marktteilnehmer import Marktteilnehmer


class Regionaltarif(BaseModel):
    """
    .. raw:: html

        <object data="../_static/images/bo4e/bo/Regionaltarif.svg" type="image/svg+xml"></object>

    .. HINT::
        `Regionaltarif JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/{__gh_version__}/src/bo4e_schemas/bo/Regionaltarif.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.REGIONALTARIF, alias="_typ")
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
    preisgarantien: Optional[list["RegionalePreisgarantie"]] = Field(default=None, title="Preisgarantien")
    preisstand: Optional[datetime] = Field(default=None, title="Preisstand")
    registeranzahl: Optional[Registeranzahl] = None
    """
    Die Art des Tarifes, z.B. Eintarif oder Mehrtarif
    """
    sparte: Optional[Sparte] = None
    """
    Strom oder Gas, etc.
    """
    tarif_auf_abschlaege: Optional[list["RegionalerAufAbschlag"]] = Field(
        default=None, alias="tarifAufAbschlaege", title="Tarifaufabschlaege"
    )
    tarifeinschraenkung: Optional["Tarifeinschraenkung"] = None
    tarifmerkmale: Optional[list[Tarifmerkmal]] = Field(default=None, title="Tarifmerkmale")
    """
    Weitere Merkmale des Tarifs, z.B. Festpreis oder Vorkasse
    """
    tarifpreise: Optional[list["RegionaleTarifpreisposition"]] = Field(default=None, title="Tarifpreise")
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
