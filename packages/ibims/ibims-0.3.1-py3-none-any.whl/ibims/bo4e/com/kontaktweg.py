from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.kontaktart import Kontaktart

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Kontaktweg(BaseModel):
    """
    Die Komponente wird dazu verwendet, die Kontaktwege innerhalb des BOs Person darzustellen

    .. raw:: html

        <object data="../_static/images/bo4e/com/Kontakt.svg" type="image/svg+xml"></object>

    .. HINT::
        `Kontakt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Kontakt.json>`_
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
    beschreibung: Optional[str] = Field(default=None, title="Beschreibung")
    """
    Spezifikation, beispielsweise "Durchwahl", "Sammelnummer" etc.
    """
    ist_bevorzugter_kontaktweg: Optional[bool] = Field(
        default=None, alias="istBevorzugterKontaktweg", title="Istbevorzugterkontaktweg"
    )
    """
    Gibt an, ob es sich um den bevorzugten Kontaktweg handelt.
    """
    kontaktart: Optional[Kontaktart] = None
    """
    Gibt die Kontaktart des Kontaktes an.
    """
    kontaktwert: Optional[str] = Field(default=None, title="Kontaktwert")
    """
    Die Nummer oder E-Mail-Adresse.
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
