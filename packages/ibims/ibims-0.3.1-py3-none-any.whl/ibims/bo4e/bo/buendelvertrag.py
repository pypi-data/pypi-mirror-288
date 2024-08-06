from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.sparte import Sparte
from ..enum.typ import Typ
from ..enum.vertragsart import Vertragsart
from ..enum.vertragsstatus import Vertragsstatus

if TYPE_CHECKING:
    from ..com.unterschrift import Unterschrift
    from ..com.vertragskonditionen import Vertragskonditionen
    from ..zusatz_attribut import ZusatzAttribut
    from .geschaeftspartner import Geschaeftspartner
    from .vertrag import Vertrag


class Buendelvertrag(BaseModel):
    """
    Abbildung eines Bündelvertrags.
    Es handelt sich hierbei um eine Liste von Einzelverträgen, die in einem Vertragsobjekt gebündelt sind.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Buendelvertrag.svg" type="image/svg+xml"></object>

    .. HINT::
        `Buendelvertrag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Buendelvertrag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.BUENDELVERTRAG, alias="_typ")
    """
    Der Typ des Geschäftsobjektes
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    beschreibung: Optional[str] = Field(default=None, title="Beschreibung")
    """
    Beschreibung zum Vertrag
    """
    einzelvertraege: Optional[list["Vertrag"]] = Field(default=None, title="Einzelvertraege")
    """
    Die Liste mit den Einzelverträgen zu den Abnahmestellen
    """
    sparte: Optional[Sparte] = None
    """
    Unterscheidungsmöglichkeiten für die Sparte
    """
    unterzeichnervp1: Optional[list["Unterschrift"]] = Field(default=None, title="Unterzeichnervp1")
    """
    Unterzeichner des Vertragspartners1
    """
    unterzeichnervp2: Optional[list["Unterschrift"]] = Field(default=None, title="Unterzeichnervp2")
    """
    Unterzeichner des Vertragspartners2
    """
    vertragsart: Optional[Vertragsart] = None
    """
    Hier ist festgelegt, um welche Art von Vertrag es sich handelt. Z.B. Netznutzungvertrag
    """
    vertragsbeginn: Optional[datetime] = Field(default=None, title="Vertragsbeginn")
    """
    Gibt an, wann der Vertrag beginnt (inklusiv)
    """
    vertragsende: Optional[datetime] = Field(default=None, title="Vertragsende")
    """
    Gibt an, wann der Vertrag (voraussichtlich) endet oder beendet wurde (exklusiv)
    """
    vertragskonditionen: Optional[list["Vertragskonditionen"]] = Field(default=None, title="Vertragskonditionen")
    """
    Festlegungen zu Laufzeiten und Kündigungsfristen
    """
    vertragsnummer: Optional[str] = Field(default=None, title="Vertragsnummer")
    """
    Eine im Verwendungskontext eindeutige Nummer für den Vertrag
    """
    vertragspartner1: Optional["Geschaeftspartner"] = None
    """
    Beispiel: "Vertrag zwischen Vertagspartner 1 ..."
    """
    vertragspartner2: Optional["Geschaeftspartner"] = None
    """
    Beispiel "Vertrag zwischen Vertagspartner 1 und Vertragspartner 2"
    """
    vertragsstatus: Optional[Vertragsstatus] = None
    """
    Gibt den Status des Vertrages an
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
