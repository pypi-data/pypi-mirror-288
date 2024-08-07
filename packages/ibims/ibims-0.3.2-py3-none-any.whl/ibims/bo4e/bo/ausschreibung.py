from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.ausschreibungsportal import Ausschreibungsportal
from ..enum.ausschreibungsstatus import Ausschreibungsstatus
from ..enum.ausschreibungstyp import Ausschreibungstyp
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.ausschreibungslos import Ausschreibungslos
    from ..com.zeitraum import Zeitraum
    from ..zusatz_attribut import ZusatzAttribut
    from .geschaeftspartner import Geschaeftspartner


class Ausschreibung(BaseModel):
    """
    Das BO Ausschreibung dient zur detaillierten Darstellung von ausgeschriebenen Energiemengen in der Energiewirtschaft

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Ausschreibung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ausschreibung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Ausschreibung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.AUSSCHREIBUNG, alias="_typ")
    """
    Vom Herausgeber der Ausschreibung vergebene eindeutige Nummer
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    abgabefrist: Optional["Zeitraum"] = None
    ausschreibender: Optional["Geschaeftspartner"] = None
    ausschreibungportal: Optional[Ausschreibungsportal] = None
    """
    Aufzählung der unterstützten Ausschreibungsportale
    """
    ausschreibungsnummer: Optional[str] = Field(default=None, title="Ausschreibungsnummer")
    """
    Vom Herausgeber der Ausschreibung vergebene eindeutige Nummer
    """
    ausschreibungsstatus: Optional[Ausschreibungsstatus] = None
    """
    Bezeichnungen für die Ausschreibungsphasen
    """
    ausschreibungstyp: Optional[Ausschreibungstyp] = None
    """
    Aufzählung für die Typisierung von Ausschreibungen
    """
    bindefrist: Optional["Zeitraum"] = None
    """
    Die einzelnen Lose, aus denen sich die Ausschreibung zusammensetzt
    """
    ist_kostenpflichtig: Optional[bool] = Field(default=None, alias="istKostenpflichtig", title="Istkostenpflichtig")
    """
    Kennzeichen, ob die Ausschreibung kostenpflichtig ist
    """
    lose: Optional[list["Ausschreibungslos"]] = Field(default=None, title="Lose")
    """
    Die einzelnen Lose, aus denen sich die Ausschreibung zusammensetzt
    """
    veroeffentlichungszeitpunkt: Optional[datetime] = Field(default=None, title="Veroeffentlichungszeitpunkt")
    """
    Gibt den Veröffentlichungszeitpunkt der Ausschreibung an
    """
    webseite: Optional[str] = Field(default=None, title="Webseite")
    """
    Internetseite, auf der die Ausschreibung veröffentlicht wurde (falls vorhanden)
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
