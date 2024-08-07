from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .tarifpreisstaffel_pro_ort import TarifpreisstaffelProOrt


class TarifpreispositionProOrt(BaseModel):
    """
    Mit dieser Komponente können Tarifpreise verschiedener Typen abgebildet werden

    .. raw:: html

        <object data="../_static/images/bo4e/com/TarifpreispositionProOrt.svg" type="image/svg+xml"></object>

    .. HINT::
        `TarifpreispositionProOrt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/TarifpreispositionProOrt.json>`_
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
    netznr: Optional[str] = Field(default=None, title="Netznr")
    """
    ene't-Netznummer des Netzes in dem der Preis gilt
    """
    ort: Optional[str] = Field(default=None, title="Ort")
    """
    Ort für den der Preis gilt
    """
    postleitzahl: Optional[str] = Field(default=None, title="Postleitzahl")
    """
    Postleitzahl des Ortes für den der Preis gilt
    """
    preisstaffeln: Optional[list["TarifpreisstaffelProOrt"]] = Field(default=None, title="Preisstaffeln")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
