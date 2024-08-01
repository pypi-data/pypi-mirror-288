from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.abgabe_art import AbgabeArt

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Konzessionsabgabe(BaseModel):
    """
    Diese Komponente wird zur Übertagung der Details zu einer Konzessionsabgabe verwendet.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Konzessionsabgabe.svg" type="image/svg+xml"></object>

    .. HINT::
        `Konzessionsabgabe JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Konzessionsabgabe.json>`_
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
    kategorie: Optional[str] = Field(default=None, title="Kategorie")
    """
    Gebührenkategorie der Konzessionsabgabe
    """
    kosten: Optional[Decimal] = Field(default=None, title="Kosten")
    """
    Konzessionsabgabe in E/kWh
    """
    satz: Optional[AbgabeArt] = None
    """
    Art der Abgabe
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
