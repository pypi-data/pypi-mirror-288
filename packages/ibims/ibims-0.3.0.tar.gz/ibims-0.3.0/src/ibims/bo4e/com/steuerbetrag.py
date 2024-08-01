from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.steuerkennzeichen import Steuerkennzeichen
from ..enum.waehrungscode import Waehrungscode

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Steuerbetrag(BaseModel):
    """
    Abbildung eines Steuerbetrages.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Steuerbetrag.svg" type="image/svg+xml"></object>

    .. HINT::
        `Steuerbetrag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Steuerbetrag.json>`_
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
    basiswert: Decimal = Field(..., title="Basiswert")
    """
    Nettobetrag für den die Steuer berechnet wurde. Z.B. 100
    """
    steuerkennzeichen: Optional[Steuerkennzeichen] = None
    """
    Kennzeichnung des Steuersatzes, bzw. Verfahrens.
    """
    steuerwert: Decimal = Field(..., title="Steuerwert")
    """
    Aus dem Basiswert berechnete Steuer. Z.B. 19 (bei UST_19)
    """
    waehrung: Optional[Waehrungscode] = None
    """
    Währung. Z.B. Euro.
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    steuerwert_vorausgezahlt: Optional[Decimal] = Field(
        default=None, alias="steuerwertVorausgezahlt", title="Steuerwertvorausgezahlt"
    )
