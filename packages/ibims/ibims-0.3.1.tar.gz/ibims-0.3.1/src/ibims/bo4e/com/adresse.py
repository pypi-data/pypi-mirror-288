from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.landescode import Landescode

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Adresse(BaseModel):
    """
    Contains an address that can be used for most purposes.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Adresse.svg" type="image/svg+xml"></object>

    .. HINT::
        `Adresse JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Adresse.json>`_
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
    adresszusatz: Optional[str] = Field(default=None, title="Adresszusatz")
    """
    Zusatzhinweis zum Auffinden der Adresse, z.B. "3. Stock linke Wohnung"
    """
    co_ergaenzung: Optional[str] = Field(default=None, alias="coErgaenzung", title="Coergaenzung")
    """
    Im Falle einer c/o-Adresse steht in diesem Attribut die Anrede. Z.B. "c/o Veronica Hauptmieterin"
    """
    hausnummer: Optional[str] = Field(default=None, title="Hausnummer")
    """
    Hausnummer inkl. Zusatz; z.B. "3", "4a"
    """
    landescode: Optional[Landescode] = Landescode.DE
    """
    Offizieller ISO-Landescode
    """
    ort: str = Field(..., title="Ort")
    """
    Bezeichnung der Stadt; z.B. "Hückelhoven"
    """
    ortsteil: Optional[str] = Field(default=None, title="Ortsteil")
    """
    Bezeichnung des Ortsteils; z.B. "Mitte"
    """
    postfach: Optional[str] = Field(default=None, title="Postfach")
    """
    Im Falle einer Postfachadresse das Postfach; Damit werden Straße und Hausnummer nicht berücksichtigt
    """
    postleitzahl: str = Field(..., title="Postleitzahl")
    """
    Die Postleitzahl; z.B: "41836"
    """
    strasse: Optional[str] = Field(default=None, title="Strasse")
    """
    Bezeichnung der Straße; z.B. "Weserstraße"
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
