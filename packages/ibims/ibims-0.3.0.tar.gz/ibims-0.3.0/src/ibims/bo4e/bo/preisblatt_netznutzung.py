from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.bilanzierungsmethode import Bilanzierungsmethode
from ..enum.kundengruppe import Kundengruppe
from ..enum.netzebene import Netzebene
from ..enum.preisstatus import Preisstatus
from ..enum.sparte import Sparte
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.preisposition import Preisposition
    from ..com.zeitraum import Zeitraum
    from ..zusatz_attribut import ZusatzAttribut
    from .marktteilnehmer import Marktteilnehmer


class PreisblattNetznutzung(BaseModel):
    """
    Die Variante des Preisblattmodells zur Abbildung der Netznutzungspreise

    .. raw:: html

        <object data="../_static/images/bo4e/bo/PreisblattNetznutzung.svg" type="image/svg+xml"></object>

    .. HINT::
        `PreisblattNetznutzung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/PreisblattNetznutzung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.PREISBLATTNETZNUTZUNG, alias="_typ")
    """
    Die Preise gelten für Marktlokationen der angebebenen Bilanzierungsmethode
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    """
    Eine Bezeichnung für das Preisblatt
    """
    bilanzierungsmethode: Optional[Bilanzierungsmethode] = None
    """
    Die Preise gelten für Marktlokationen der angebebenen Bilanzierungsmethode
    """
    gueltigkeit: Optional["Zeitraum"] = None
    """
    Der Zeitraum für den der Preis festgelegt ist
    """
    herausgeber: Optional["Marktteilnehmer"] = None
    """
    Der Netzbetreiber, der die Preise veröffentlicht hat
    """
    kundengruppe: Optional[Kundengruppe] = None
    netzebene: Optional[Netzebene] = None
    """
    Die Preise gelten für Marktlokationen in der angebebenen Netzebene
    """
    preispositionen: Optional[list["Preisposition"]] = Field(default=None, title="Preispositionen")
    """
    Die einzelnen Positionen, die mit dem Preisblatt abgerechnet werden können. Z.B. Arbeitspreis, Grundpreis etc
    """
    preisstatus: Optional[Preisstatus] = None
    """
    Merkmal, das anzeigt, ob es sich um vorläufige oder endgültige Preise handelt
    """
    sparte: Optional[Sparte] = None
    """
    Preisblatt gilt für angegebene Sparte
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
