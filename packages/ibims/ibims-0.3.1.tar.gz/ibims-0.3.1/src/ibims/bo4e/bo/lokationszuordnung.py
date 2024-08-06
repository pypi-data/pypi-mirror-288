from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.zeitspanne import Zeitspanne
    from ..zusatz_attribut import ZusatzAttribut
    from .marktlokation import Marktlokation
    from .messlokation import Messlokation
    from .netzlokation import Netzlokation
    from .steuerbare_ressource import SteuerbareRessource
    from .technische_ressource import TechnischeRessource


class Lokationszuordnung(BaseModel):
    """
    Modell für die Abbildung der Referenz auf die Lokationsbündelstruktur. Diese gibt an welche Marktlokationen,
    Messlokationen, Netzlokationen, technische/steuerbaren Ressourcen an einer Lokation vorhanden sind.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Lokationszuordnung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Lokationszuordnung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Lokationszuordnung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.LOKATIONSZUORDNUNG, alias="_typ")
    """
    Liste mit referenzierten Marktlokationen
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    gueltigkeit: Optional["Zeitspanne"] = None
    """
    Zeitspanne der Gültigkeit
    """
    lokationsbuendelcode: Optional[str] = Field(default=None, title="Lokationsbuendelcode")
    """
    Code, der angibt wie die Lokationsbündelstruktur zusammengesetzt ist (zu finden unter "Codeliste der Lokationsbündelstrukturen" auf https://www.edi-energy.de/index.php?id=38)
    """
    marktlokationen: Optional[list["Marktlokation"]] = Field(default=None, title="Marktlokationen")
    """
    Liste mit referenzierten Marktlokationen
    """
    messlokationen: Optional[list["Messlokation"]] = Field(default=None, title="Messlokationen")
    """
    Liste mit referenzierten Messlokationen
    """
    netzlokationen: Optional[list["Netzlokation"]] = Field(default=None, title="Netzlokationen")
    """
    Liste mit referenzierten Netzlokationen
    """
    steuerbare_ressourcen: Optional[list["SteuerbareRessource"]] = Field(
        default=None, alias="steuerbareRessourcen", title="Steuerbareressourcen"
    )
    """
    Liste mit referenzierten steuerbaren Ressourcen
    """
    technische_ressourcen: Optional[list["TechnischeRessource"]] = Field(
        default=None, alias="technischeRessourcen", title="Technischeressourcen"
    )
    """
    Liste mit referenzierten technischen Ressourcen
    """
    zuordnungstyp: Optional[str] = Field(default=None, title="Zuordnungstyp")
    """
    Verknüpfungsrichtung z.B. Malo-Melo [TODO: Eventuell anderer Datentyp]
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
