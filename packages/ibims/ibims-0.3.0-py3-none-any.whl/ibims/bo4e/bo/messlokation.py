from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.netzebene import Netzebene
from ..enum.sparte import Sparte
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.adresse import Adresse
    from ..com.dienstleistung import Dienstleistung
    from ..com.geokoordinaten import Geokoordinaten
    from ..com.katasteradresse import Katasteradresse
    from ..zusatz_attribut import ZusatzAttribut
    from .geraet import Geraet
    from .lokationszuordnung import Lokationszuordnung
    from .zaehler import Zaehler


class Messlokation(BaseModel):
    """
    Object containing information about a Messlokation

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Messlokation.svg" type="image/svg+xml"></object>

    .. HINT::
        `Messlokation JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Messlokation.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.MESSLOKATION, alias="_typ")
    """
    Die Messlokations-Identifikation; Das ist die frühere Zählpunktbezeichnung
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    geoadresse: Optional["Geokoordinaten"] = None
    geraete: Optional[list["Geraet"]] = Field(default=None, title="Geraete")
    """
    Liste der Geräte, die zu dieser Messstelle gehört
    """
    grundzustaendiger_msb_codenr: Optional[str] = Field(
        default=None, alias="grundzustaendigerMsbCodenr", title="Grundzustaendigermsbcodenr"
    )
    grundzustaendiger_msbim_codenr: Optional[str] = Field(
        default=None, alias="grundzustaendigerMsbimCodenr", title="Grundzustaendigermsbimcodenr"
    )
    katasterinformation: Optional["Katasteradresse"] = None
    """
    Lokationszuordnung, um bspw. die zugehörigen Marktlokationen anzugeben
    """
    lokationsbuendel_objektcode: Optional[str] = Field(
        default=None, alias="lokationsbuendelObjektcode", title="Lokationsbuendelobjektcode"
    )
    """
    Lokationsbuendel Code, der die Funktion dieses BOs an der Lokationsbuendelstruktur beschreibt.
    """
    lokationszuordnungen: Optional[list["Lokationszuordnung"]] = Field(default=None, title="Lokationszuordnungen")
    """
    Lokationszuordnung, um bspw. die zugehörigen Marktlokationen anzugeben
    """
    messadresse: Optional["Adresse"] = None
    messdienstleistung: Optional[list["Dienstleistung"]] = Field(default=None, title="Messdienstleistung")
    """
    Liste der Messdienstleistungen, die zu dieser Messstelle gehört
    """
    messgebietnr: Optional[str] = Field(default=None, title="Messgebietnr")
    """
    Die Nummer des Messgebietes in der ene't-Datenbank
    """
    messlokations_id: str = Field(..., alias="messlokationsId", title="Messlokationsid")
    """
    Die Messlokations-Identifikation; Das ist die frühere Zählpunktbezeichnung
    """
    messlokationszaehler: Optional[list["Zaehler"]] = Field(default=None, title="Messlokationszaehler")
    """
    Zähler, die zu dieser Messlokation gehören
    """
    netzebene_messung: Optional[Netzebene] = Field(default=None, alias="netzebeneMessung")
    """
    Spannungsebene der Messung
    """
    sparte: Optional[Sparte] = None
    """
    Sparte der Messlokation, z.B. Gas oder Strom
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
