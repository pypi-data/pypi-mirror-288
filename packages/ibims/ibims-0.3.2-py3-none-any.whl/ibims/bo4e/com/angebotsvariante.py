from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.angebotsstatus import Angebotsstatus

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .angebotsteil import Angebotsteil
    from .betrag import Betrag
    from .menge import Menge


class Angebotsvariante(BaseModel):
    """
    Führt die verschiedenen Ausprägungen der Angebotsberechnung auf

    .. raw:: html

        <object data="../_static/images/bo4e/com/Angebotsvariante.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebotsvariante JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Angebotsvariante.json>`_
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
    angebotsstatus: Optional[Angebotsstatus] = None
    """
    Gibt den Status eines Angebotes an.
    """
    bindefrist: Optional[datetime] = Field(default=None, title="Bindefrist")
    """
    Bis zu diesem Zeitpunkt gilt die Angebotsvariante
    """
    erstellungsdatum: Optional[datetime] = Field(default=None, title="Erstellungsdatum")
    """
    Datum der Erstellung der Angebotsvariante
    """
    gesamtkosten: Optional["Betrag"] = None
    """
    Aufsummierte Kosten aller Angebotsteile
    """
    gesamtmenge: Optional["Menge"] = None
    """
    Aufsummierte Wirkarbeitsmenge aller Angebotsteile
    """
    teile: Optional[list["Angebotsteil"]] = Field(default=None, title="Teile")
    """
    Angebotsteile werden im einfachsten Fall für eine Marktlokation oder Lieferstellenadresse erzeugt.
    Hier werden die Mengen und Gesamtkosten aller Angebotspositionen zusammengefasst.
    Eine Variante besteht mindestens aus einem Angebotsteil.
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
