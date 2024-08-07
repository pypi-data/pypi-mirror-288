from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..bo.marktteilnehmer import Marktteilnehmer
    from ..zusatz_attribut import ZusatzAttribut


class Konfigurationsprodukt(BaseModel):
    """
    Object containing information about a Konfigurationsprodukt

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Konfigurationsprodukt.svg" type="image/svg+xml"></object>

    .. HINT::
        `Konfigurationsprodukt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Konfigurationsprodukt.json>`_
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
    leistungskurvendefinition: Optional[str] = Field(default=None, title="Leistungskurvendefinition")
    marktpartner: Optional["Marktteilnehmer"] = None
    produktcode: Optional[str] = Field(default=None, title="Produktcode")
    schaltzeitdefinition: Optional[str] = Field(default=None, title="Schaltzeitdefinition")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
