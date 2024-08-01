from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.themengebiet import Themengebiet

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Zustaendigkeit(BaseModel):
    """
    Enthält die zeitliche Zuordnung eines Ansprechpartners zu Abteilungen und Zuständigkeiten.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zustaendigkeit.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zustaendigkeit JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Zustaendigkeit.json>`_
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
    abteilung: Optional[str] = Field(default=None, title="Abteilung")
    """
    Berufliche Rolle des Ansprechpartners/ der Person
    """
    position: Optional[str] = Field(default=None, title="Position")
    """
    Berufliche Rolle des Ansprechpartners/ der Person
    """
    themengebiet: Optional[Themengebiet] = None
    """
    Hier kann eine thematische Zuordnung des Ansprechpartners bzw. der Person angegeben werden
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
