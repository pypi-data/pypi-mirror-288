from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.marktrolle import Marktrolle
from ..enum.rollencodetyp import Rollencodetyp
from ..enum.sparte import Sparte
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .geschaeftspartner import Geschaeftspartner


class Marktteilnehmer(BaseModel):
    """
    Objekt zur Aufnahme der Information zu einem Marktteilnehmer

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Marktteilnehmer.svg" type="image/svg+xml"></object>

    .. HINT::
        `Marktteilnehmer JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Marktteilnehmer.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.MARKTTEILNEHMER, alias="_typ")
    """
    Gibt im Klartext die Bezeichnung der Marktrolle an
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    geschaeftspartner: Optional["Geschaeftspartner"] = None
    """
    Der zu diesem Marktteilnehmer gehörende Geschäftspartner
    """
    makoadresse: Optional[list[str]] = Field(default=None, title="Makoadresse")
    """
    Die 1:1-Kommunikationsadresse des Marktteilnehmers. Diese wird in der Marktkommunikation verwendet. Konkret kann dies eine eMail-Adresse oder ein AS4-Endpunkt sein.
    """
    marktrolle: Optional[Marktrolle] = None
    """
    Gibt im Klartext die Bezeichnung der Marktrolle an
    """
    rollencodenummer: Optional[str] = Field(default=None, title="Rollencodenummer")
    """
    Gibt die Codenummer der Marktrolle an
    """
    rollencodetyp: Optional[Rollencodetyp] = None
    """
    Gibt den Typ des Codes an
    """
    sparte: Optional[Sparte] = None
    """
    Sparte des Marktteilnehmers, z.B. Gas oder Strom
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
