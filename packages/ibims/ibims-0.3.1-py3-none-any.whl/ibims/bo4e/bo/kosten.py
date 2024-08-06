from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.kostenklasse import Kostenklasse
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.betrag import Betrag
    from ..com.kostenblock import Kostenblock
    from ..com.zeitraum import Zeitraum
    from ..zusatz_attribut import ZusatzAttribut


class Kosten(BaseModel):
    """
    Dieses BO wird zur Übertagung von hierarchischen Kostenstrukturen verwendet.
    Die Kosten werden dabei in Kostenblöcke und diese wiederum in Kostenpositionen strukturiert.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Kosten.svg" type="image/svg+xml"></object>

    .. HINT::
        `Kosten JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Kosten.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.KOSTEN, alias="_typ")
    """
    Klasse der Kosten, beispielsweise Fremdkosten
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    gueltigkeit: Optional["Zeitraum"] = None
    """
    Für diesen Zeitraum wurden die Kosten ermittelt
    """
    kostenbloecke: Optional[list["Kostenblock"]] = Field(default=None, title="Kostenbloecke")
    """
    In Kostenblöcken werden Kostenpositionen zusammengefasst. Beispiele: Netzkosten, Umlagen, Steuern etc
    """
    kostenklasse: Optional[Kostenklasse] = None
    """
    Klasse der Kosten, beispielsweise Fremdkosten
    """
    summe_kosten: Optional[list["Betrag"]] = Field(default=None, alias="summeKosten", title="Summekosten")
    """
    Die Gesamtsumme über alle Kostenblöcke und -positionen
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
