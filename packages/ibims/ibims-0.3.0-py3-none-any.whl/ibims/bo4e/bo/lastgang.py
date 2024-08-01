from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.mengeneinheit import Mengeneinheit
from ..enum.sparte import Sparte
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.menge import Menge
    from ..com.zeitreihenwert import Zeitreihenwert
    from ..zusatz_attribut import ZusatzAttribut
    from .marktlokation import Marktlokation
    from .messlokation import Messlokation


class Lastgang(BaseModel):
    """
    Modell zur Abbildung eines Lastganges;
    In diesem Modell werden die Messwerte mit einem vollständigen Zeitintervall (zeit_intervall_laenge) angegeben und es bietet daher eine hohe Flexibilität in der Übertragung jeglicher zeitlich veränderlicher Messgrössen.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Lastgang.svg" type="image/svg+xml"></object>

    .. HINT::
        `Lastgang JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Lastgang.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.LASTGANG, alias="_typ")
    """
    Angabe, ob es sich um einen Gas- oder Stromlastgang handelt
    """
    marktlokation: Optional["Marktlokation"] = None
    """
    Marktlokation, zu der der Lastgang gehört
    """
    messgroesse: Optional[Mengeneinheit] = None
    """
    Definition der gemessenen Größe anhand ihrer Einheit
    """
    messlokation: Optional["Messlokation"] = None
    """
    Marktlokation, zu der der Lastgang gehört
    """
    obis_kennzahl: Optional[str] = Field(default=None, alias="obisKennzahl", title="Obiskennzahl")
    """
    Die OBIS-Kennzahl für den Wert, die festlegt, welche Größe mit dem Stand gemeldet wird, z.B. '1-0:1.8.1'
    """
    sparte: Optional[Sparte] = None
    """
    Angabe, ob es sich um einen Gas- oder Stromlastgang handelt
    """
    version: Optional[str] = Field(default=None, title="Version")
    """
    Versionsnummer des Lastgangs
    """
    werte: Optional[list["Zeitreihenwert"]] = Field(default=None, title="Werte")
    """
    Die im Lastgang enthaltenen Messwerte
    """
    zeit_intervall_laenge: Optional["Menge"] = Field(..., alias="zeitIntervallLaenge")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
