from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.standorteigenschaften_gas import StandorteigenschaftenGas
    from ..com.standorteigenschaften_strom import StandorteigenschaftenStrom
    from ..zusatz_attribut import ZusatzAttribut


class Standorteigenschaften(BaseModel):
    """
    Modelliert die regionalen und spartenspezifischen Eigenschaften einer gegebenen Adresse.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Standorteigenschaften.svg" type="image/svg+xml"></object>

    .. HINT::
        `Standorteigenschaften JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Standorteigenschaften.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.STANDORTEIGENSCHAFTEN, alias="_typ")
    """
    Eigenschaften zur Sparte Strom
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    eigenschaften_gas: Optional["StandorteigenschaftenGas"] = Field(default=None, alias="eigenschaftenGas")
    """
    Eigenschaften zur Sparte Gas
    """
    eigenschaften_strom: Optional[list["StandorteigenschaftenStrom"]] = Field(
        default=None, alias="eigenschaftenStrom", title="Eigenschaftenstrom"
    )
    """
    Eigenschaften zur Sparte Strom
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
