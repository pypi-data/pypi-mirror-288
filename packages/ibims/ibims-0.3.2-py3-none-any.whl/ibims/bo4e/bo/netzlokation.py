from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.marktrolle import Marktrolle
from ..enum.sparte import Sparte
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.konfigurationsprodukt import Konfigurationsprodukt
    from ..com.menge import Menge
    from ..com.verwendungszweck_pro_marktrolle import VerwendungszweckProMarktrolle
    from ..zusatz_attribut import ZusatzAttribut
    from .lokationszuordnung import Lokationszuordnung


class Netzlokation(BaseModel):
    """
    Object containing information about a Netzlokation

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Netzlokation.svg" type="image/svg+xml"></object>

    .. HINT::
        `Netzlokation JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Netzlokation.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.NETZLOKATION, alias="_typ")
    """
    Identifikationsnummer einer Netzlokation, an der Energie entweder verbraucht, oder erzeugt wird
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    eigenschaft_msb_lokation: Optional[Marktrolle] = Field(default=None, alias="eigenschaftMsbLokation")
    """
    Eigenschaft des Messstellenbetreibers an der Lokation
    """
    grundzustaendiger_msb_codenr: Optional[str] = Field(
        default=None, alias="grundzustaendigerMsbCodenr", title="Grundzustaendigermsbcodenr"
    )
    """
    Codenummer des grundzuständigen Messstellenbetreibers, der für diese Netzlokation zuständig ist.
    """
    konfigurationsprodukte: Optional[list["Konfigurationsprodukt"]] = Field(
        default=None, title="Konfigurationsprodukte"
    )
    """
    Produkt-Daten der Netzlokation
    """
    lokationsbuendel_objektcode: Optional[str] = Field(
        default=None, alias="lokationsbuendelObjektcode", title="Lokationsbuendelobjektcode"
    )
    """
    Lokationsbuendel Code, der die Funktion dieses BOs an der Lokationsbuendelstruktur beschreibt.
    """
    lokationszuordnungen: Optional[list["Lokationszuordnung"]] = Field(default=None, title="Lokationszuordnungen")
    """
    Lokationszuordnung, um bspw. die zugehörigen Messlokationen anzugeben
    """
    netzanschlussleistung: Optional["Menge"] = None
    """
    Netzanschlussleistungsmenge der Netzlokation
    """
    netzlokations_id: Optional[str] = Field(default=None, alias="netzlokationsId", title="Netzlokationsid")
    """
    Identifikationsnummer einer Netzlokation, an der Energie entweder verbraucht, oder erzeugt wird
    """
    obiskennzahl: Optional[str] = Field(default=None, title="Obiskennzahl")
    """
    Die OBIS-Kennzahl für die Netzlokation
    """
    sparte: Optional[Sparte] = None
    """
    Sparte der Netzlokation, z.B. Gas oder Strom.
    """
    steuerkanal: Optional[bool] = Field(default=None, title="Steuerkanal")
    """
    Ob ein Steuerkanal der Netzlokation zugeordnet ist und somit die Netzlokation gesteuert werden kann.
    """
    verwendungszweck: Optional["VerwendungszweckProMarktrolle"] = None
    """
    Verwendungungszweck der Werte Netzlokation
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
