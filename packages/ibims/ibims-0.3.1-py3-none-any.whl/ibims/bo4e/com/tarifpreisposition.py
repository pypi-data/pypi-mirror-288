from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.mengeneinheit import Mengeneinheit
from ..enum.preistyp import Preistyp
from ..enum.waehrungseinheit import Waehrungseinheit

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .preisstaffel import Preisstaffel


class Tarifpreisposition(BaseModel):
    """
    Mit dieser Komponente können Tarifpreise verschiedener Typen abgebildet werden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifpreisposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifpreisposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Tarifpreisposition.json>`_
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
    bezugseinheit: Optional[Mengeneinheit] = None
    """
    Größe, auf die sich die Einheit bezieht, beispielsweise kWh, Jahr
    """
    einheit: Optional[Waehrungseinheit] = None
    """
    Einheit des Preises (z.B. EURO)
    """
    mengeneinheitstaffel: Optional[Mengeneinheit] = None
    """
    Gibt an, nach welcher Menge die vorgenannte Einschränkung erfolgt (z.B. Jahresstromverbrauch in kWh)
    """
    preisstaffeln: Optional[list["Preisstaffel"]] = Field(default=None, title="Preisstaffeln")
    """
    Hier sind die Staffeln mit ihren Preisenangaben definiert
    """
    preistyp: Optional[Preistyp] = None
    """
    Angabe des Preistypes (z.B. Grundpreis)
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
