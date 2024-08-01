from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class TarifpreisstaffelProOrt(BaseModel):
    """
    Gibt die Staffelgrenzen der jeweiligen Preise an

    .. raw:: html

        <object data="../_static/images/bo4e/com/TarifpreisstaffelProOrt.svg" type="image/svg+xml"></object>

    .. HINT::
        `TarifpreisstaffelProOrt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/TarifpreisstaffelProOrt.json>`_
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
    arbeitspreis: Optional[Decimal] = Field(default=None, title="Arbeitspreis")
    """
    Der Arbeitspreis in ct/kWh
    """
    arbeitspreis_nt: Optional[Decimal] = Field(default=None, alias="arbeitspreisNT", title="Arbeitspreisnt")
    """
    Der Arbeitspreis für Verbräuche in der Niedertarifzeit in ct/kWh
    """
    grundpreis: Optional[Decimal] = Field(default=None, title="Grundpreis")
    """
    Der Grundpreis in Euro/Jahr
    """
    staffelgrenze_bis: Optional[Decimal] = Field(default=None, alias="staffelgrenzeBis", title="Staffelgrenzebis")
    """
    Oberer Wert, bis zu dem die Staffel gilt (exklusive)
    """
    staffelgrenze_von: Optional[Decimal] = Field(default=None, alias="staffelgrenzeVon", title="Staffelgrenzevon")
    """
    Unterer Wert, ab dem die Staffel gilt (inklusive)
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
