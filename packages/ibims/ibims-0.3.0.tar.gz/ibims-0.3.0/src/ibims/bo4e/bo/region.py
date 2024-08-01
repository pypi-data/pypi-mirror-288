from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.regionskriterium import Regionskriterium
    from ..zusatz_attribut import ZusatzAttribut


class Region(BaseModel):
    """
    Modellierung einer Region als Menge von Kriterien, die eine Region beschreiben

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Region.svg" type="image/svg+xml"></object>

    .. HINT::
        `Region JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Region.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.REGION, alias="_typ")
    """
    Bezeichnung der Region
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    """
    Bezeichnung der Region
    """
    negativ_liste: Optional[list["Regionskriterium"]] = Field(default=None, alias="negativListe", title="Negativliste")
    """
    Negativliste der Kriterien zur Definition der Region
    """
    positiv_liste: Optional[list["Regionskriterium"]] = Field(default=None, alias="positivListe", title="Positivliste")
    """
    Positivliste der Kriterien zur Definition der Region
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
