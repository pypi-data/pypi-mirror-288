from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.medium import Medium
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.messart import Messart
from ..enum.messgroesse import Messgroesse
from ..enum.typ import Typ
from ..enum.wertermittlungsverfahren import Wertermittlungsverfahren

if TYPE_CHECKING:
    from ..com.zeitreihenwert import Zeitreihenwert
    from ..zusatz_attribut import ZusatzAttribut


class Zeitreihe(BaseModel):
    """
    Abbildung einer allgemeinen Zeitreihe mit einem Wertvektor.
    Die Werte können mit wahlfreier zeitlicher Distanz im Vektor abgelegt sein.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Zeitreihe.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitreihe JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Zeitreihe.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.ZEITREIHE, alias="_typ")
    """
    Bezeichnung für die Zeitreihe
    """
    beschreibung: Optional[str] = Field(default=None, title="Beschreibung")
    """
    Beschreibt die Verwendung der Zeitreihe
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    """
    Bezeichnung für die Zeitreihe
    """
    einheit: Optional[Mengeneinheit] = None
    """
    Alle Werte in der Tabelle haben die Einheit, die hier angegeben ist
    """
    medium: Optional[Medium] = None
    """
    Medium, das gemessen wurde (z.B. Wasser, Dampf, Strom, Gas)
    """
    messart: Optional[Messart] = None
    """
    Beschreibt die Art der Messung (z.B. aktueller Wert, mittlerer Wert, maximaler Wert)
    """
    messgroesse: Optional[Messgroesse] = None
    """
    Beschreibt, was gemessen wurde (z.B. Strom, Spannung, Wirkleistung, Scheinleistung)
    """
    version: Optional[str] = Field(default=None, title="Version")
    """
    Version der Zeitreihe
    """
    werte: Optional[list["Zeitreihenwert"]] = Field(default=None, title="Werte")
    """
    Hier liegen jeweils die Werte
    """
    wertherkunft: Optional[Wertermittlungsverfahren] = None
    """
    Kennzeichnung, wie die Werte entstanden sind, z.B. durch Messung
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
