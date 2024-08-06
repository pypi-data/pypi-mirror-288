from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.betrag import Betrag
    from ..com.fremdkostenblock import Fremdkostenblock
    from ..com.zeitraum import Zeitraum
    from ..zusatz_attribut import ZusatzAttribut


class Fremdkosten(BaseModel):
    """
    Mit diesem BO werden die Fremdkosten, beispielsweise für eine Angebotserstellung oder eine Rechnungsprüfung,
    übertragen.
    Die Fremdkosten enthalten dabei alle Kostenblöcke, die von anderen Marktteilnehmern oder Instanzen erhoben werden.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Fremdkosten.svg" type="image/svg+xml"></object>

    .. HINT::
        `Fremdkosten JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Fremdkosten.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.FREMDKOSTEN, alias="_typ")
    """
    Für diesen Zeitraum wurden die Kosten ermittelt
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    gueltigkeit: Optional["Zeitraum"] = None
    """
    Für diesen Zeitraum wurden die Kosten ermittelt
    """
    kostenbloecke: Optional[list["Fremdkostenblock"]] = Field(default=None, title="Kostenbloecke")
    """
    In Kostenblöcken werden Kostenpositionen zusammengefasst. Beispiele: Netzkosten, Umlagen, Steuern etc
    """
    summe_kosten: Optional["Betrag"] = Field(default=None, alias="summeKosten")
    """
    Die Gesamtsumme über alle Kostenblöcke und -positionen
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
