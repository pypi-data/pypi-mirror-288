from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class StandorteigenschaftenStrom(BaseModel):
    """
    Standorteigenschaften der Sparte Strom

    .. raw:: html

        <object data="../_static/images/bo4e/com/StandorteigenschaftenStrom.svg" type="image/svg+xml"></object>

    .. HINT::
        `StandorteigenschaftenStrom JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/StandorteigenschaftenStrom.json>`_
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
    bilanzierungsgebiet_eic: Optional[str] = Field(
        default=None, alias="bilanzierungsgebietEic", title="Bilanzierungsgebieteic"
    )
    """
    Die EIC-Nummer des Bilanzierungsgebietes
    """
    regelzone: Optional[str] = Field(default=None, title="Regelzone")
    """
    Der Name der Regelzone
    """
    regelzone_eic: Optional[str] = Field(default=None, alias="regelzoneEic", title="Regelzoneeic")
    """
    De EIC-Nummer der Regelzone
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
