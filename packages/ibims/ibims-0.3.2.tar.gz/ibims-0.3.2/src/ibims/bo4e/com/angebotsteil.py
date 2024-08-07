from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..bo.marktlokation import Marktlokation
    from ..zusatz_attribut import ZusatzAttribut
    from .angebotsposition import Angebotsposition
    from .betrag import Betrag
    from .menge import Menge
    from .zeitraum import Zeitraum


class Angebotsteil(BaseModel):
    """
    Mit dieser Komponente wird ein Teil einer Angebotsvariante abgebildet.
    Hier werden alle Angebotspositionen aggregiert.
    Angebotsteile werden im einfachsten Fall für eine Marktlokation oder Lieferstellenadresse erzeugt.
    Hier werden die Mengen und Gesamtkosten aller Angebotspositionen zusammengefasst.
    Eine Variante besteht mindestens aus einem Angebotsteil.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Angebotsteil.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebotsteil JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Angebotsteil.json>`_
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
    anfrage_subreferenz: Optional[str] = Field(default=None, alias="anfrageSubreferenz", title="Anfragesubreferenz")
    """
    Identifizierung eines Subkapitels einer Anfrage, beispielsweise das Los einer Ausschreibung
    """
    gesamtkostenangebotsteil: Optional["Betrag"] = None
    """
    Summe der Jahresenergiekosten aller in diesem Angebotsteil enthaltenen Lieferstellen
    """
    gesamtmengeangebotsteil: Optional["Menge"] = None
    """
    Summe der Verbräuche aller in diesem Angebotsteil eingeschlossenen Lieferstellen
    """
    lieferstellenangebotsteil: Optional[list["Marktlokation"]] = Field(default=None, title="Lieferstellenangebotsteil")
    """
    Marktlokationen, für die dieses Angebotsteil gilt, falls vorhanden.
    Durch die Marktlokation ist auch die Lieferadresse festgelegt
    """
    lieferzeitraum: Optional["Zeitraum"] = None
    """
    Hier kann der Belieferungszeitraum angegeben werden, für den dieser Angebotsteil gilt
    """
    positionen: Optional[list["Angebotsposition"]] = Field(default=None, title="Positionen")
    """
    Einzelne Positionen, die zu diesem Angebotsteil gehören
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
