from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .betrag import Betrag
    from .fremdkostenposition import Fremdkostenposition


class Fremdkostenblock(BaseModel):
    """
    Komponente zur Abbildung eines Kostenblocks in den Fremdkosten

    .. raw:: html

        <object data="../_static/images/bo4e/com/Fremdkostenblock.svg" type="image/svg+xml"></object>

    .. HINT::
        `Fremdkostenblock JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Fremdkostenblock.json>`_
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
    kostenblockbezeichnung: Optional[str] = Field(default=None, title="Kostenblockbezeichnung")
    """
    Bezeichnung für einen Kostenblock. Z.B. Netzkosten, Messkosten, Umlagen, etc.
    """
    kostenpositionen: Optional[list["Fremdkostenposition"]] = Field(default=None, title="Kostenpositionen")
    """
    Hier sind die Details zu einer Kostenposition aufgeführt. Z.B.:
    Alliander Netz Heinsberg GmbH, 2018-02-01, 2019-01-01, Arbeitspreis HT, 3.660 kWh,
    5,8200 ct/kWh, 213,01 €
    """
    summe_kostenblock: Optional["Betrag"] = Field(default=None, alias="summeKostenblock")
    """
    Die Summe aller Kostenpositionen dieses Blocks
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
