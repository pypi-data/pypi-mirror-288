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
    from ..com.vertragsteil import Vertragsteil
    from ..zusatz_attribut import ZusatzAttribut
    from .geschaeftspartner import Geschaeftspartner


class Vertrag(BaseModel):
    """
    Modell für die Abbildung von Vertragsbeziehungen;
    Das Objekt dient dazu, alle Arten von Verträgen, die in der Energiewirtschaft Verwendung finden, abzubilden.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Vertrag.svg" type="image/svg+xml"></object>

    .. HINT::
        `Vertrag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Vertrag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.VERTRAG, alias="_typ")
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
    sparte: Optional[Sparte] = None
    """
    Unterscheidungsmöglichkeiten für die Sparte
    """
    unterzeichnervp1: Optional[list["Unterschrift"]] = Field(default=None, title="Unterzeichnervp1")
    """
    Unterzeichner des Vertragspartners 1
    """
    unterzeichnervp2: Optional[list["Unterschrift"]] = Field(default=None, title="Unterzeichnervp2")
    """
    Unterzeichner des Vertragspartners 2
    """
    vertragsart: Optional[Vertragsart] = None
    """
    Hier ist festgelegt, um welche Art von Vertrag es sich handelt.
    """
    vertragsbeginn: datetime = Field(..., title="Vertragsbeginn")
    """
    Gibt an, wann der Vertrag beginnt (inklusiv)
    """
    vertragsende: Optional[datetime] = Field(default=None, title="Vertragsende")
    """
    Gibt an, wann der Vertrag (voraussichtlich) endet oder beendet wurde (exklusiv)
    """
    vertragskonditionen: Optional["Vertragskonditionen"] = None
    """
    Festlegungen zu Laufzeiten und Kündigungsfristen
    """
    vertragsnummer: str = Field(..., title="Vertragsnummer")
    """
    Eine im Verwendungskontext eindeutige Nummer für den Vertrag
    """
    vertragspartner1: "Geschaeftspartner"
    vertragspartner2: "Geschaeftspartner"
    vertragsstatus: Optional[Vertragsstatus] = None
    """
    Gibt den Status des Vertrags an
    """
    vertragsteile: Optional[list["Vertragsteil"]] = Field(default=None, title="Vertragsteile")
    """
    Beschreibung zum Vertrag
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
