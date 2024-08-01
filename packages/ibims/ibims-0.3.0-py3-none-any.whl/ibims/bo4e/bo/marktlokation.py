from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.bilanzierungsmethode import Bilanzierungsmethode
from ..enum.energierichtung import Energierichtung
from ..enum.gasqualitaet import Gasqualitaet
from ..enum.gebiettyp import Gebiettyp
from ..enum.kundentyp import Kundentyp
from ..enum.marktgebiet import Marktgebiet
from ..enum.messtechnische_einordnung import MesstechnischeEinordnung
from ..enum.netzebene import Netzebene
from ..enum.profiltyp import Profiltyp
from ..enum.prognosegrundlage import Prognosegrundlage
from ..enum.regelzone import Regelzone
from ..enum.sparte import Sparte
from ..enum.typ import Typ
from ..enum.variant import Variant
from ..enum.verbrauchsart import Verbrauchsart

if TYPE_CHECKING:
    from ..com.adresse import Adresse
    from ..com.geokoordinaten import Geokoordinaten
    from ..com.katasteradresse import Katasteradresse
    from ..com.verbrauch import Verbrauch
    from ..com.zaehlwerk import Zaehlwerk
    from ..zusatz_attribut import ZusatzAttribut
    from .geschaeftspartner import Geschaeftspartner
    from .lokationszuordnung import Lokationszuordnung


class Marktlokation(BaseModel):
    """
    Object containing information about a Marktlokation

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Marktlokation.svg" type="image/svg+xml"></object>

    .. HINT::
        `Marktlokation JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Marktlokation.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.MARKTLOKATION, alias="_typ")
    """
    Identifikationsnummer einer Marktlokation, an der Energie entweder verbraucht, oder erzeugt wird.
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    bilanzierungsgebiet: Optional[str] = Field(default=None, title="Bilanzierungsgebiet")
    """
    Bilanzierungsgebiet, dem das Netzgebiet zugeordnet ist - im Falle eines Strom Netzes
    """
    bilanzierungsmethode: Optional[Bilanzierungsmethode] = None
    """
    Die Bilanzierungsmethode, RLM oder SLP
    """
    endkunde: Optional["Geschaeftspartner"] = None
    """
    Geschäftspartner, dem diese Marktlokation gehört
    """
    energierichtung: Optional[Energierichtung] = None
    """
    Kennzeichnung, ob Energie eingespeist oder entnommen (ausgespeist) wird
    """
    gasqualitaet: Optional[Gasqualitaet] = None
    """
    Die Gasqualität in diesem Netzgebiet. H-Gas oder L-Gas. Im Falle eines Gas-Netzes
    """
    gebietstyp: Optional[Gebiettyp] = None
    """
    Typ des Netzgebietes, z.B. Verteilnetz
    """
    geoadresse: Optional["Geokoordinaten"] = None
    grundversorgercodenr: Optional[str] = Field(default=None, title="Grundversorgercodenr")
    """
    Codenummer des Grundversorgers, der für diese Marktlokation zuständig ist
    """
    ist_unterbrechbar: Optional[bool] = Field(default=None, alias="istUnterbrechbar", title="Istunterbrechbar")
    """
    Gibt an, ob es sich um eine unterbrechbare Belieferung handelt
    """
    katasterinformation: Optional["Katasteradresse"] = None
    kundengruppen: list[Kundentyp] = Field(..., title="Kundengruppen")
    """
    Kundengruppen der Marktlokation
    """
    lokationsadresse: Optional["Adresse"] = None
    """
    Die Adresse, an der die Energie-Lieferung oder -Einspeisung erfolgt
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
    marktgebiet: Optional[Marktgebiet] = None
    marktlokations_id: str = Field(..., alias="marktlokationsId", title="Marktlokationsid")
    """
    Identifikationsnummer einer Marktlokation, an der Energie entweder verbraucht, oder erzeugt wird.
    """
    netzbetreibercodenr: Optional[str] = Field(default=None, title="Netzbetreibercodenr")
    """
    Codenummer des Netzbetreibers, an dessen Netz diese Marktlokation angeschlossen ist.
    """
    netzebene: Optional[Netzebene] = None
    netzgebietsnr: Optional[str] = Field(default=None, title="Netzgebietsnr")
    """
    Die ID des Gebietes in der ene't-Datenbank
    """
    regelzone: Optional[str] = Field(default=None, title="Regelzone")
    """
    Kundengruppen der Marktlokation
    """
    sparte: Sparte
    """
    Sparte der Marktlokation, z.B. Gas oder Strom
    """
    verbrauchsart: Optional[Verbrauchsart] = None
    """
    Verbrauchsart der Marktlokation.
    """
    verbrauchsmengen: Optional[list["Verbrauch"]] = Field(default=None, title="Verbrauchsmengen")
    zaehlwerke: Optional[list["Zaehlwerk"]] = Field(default=None, title="Zaehlwerke")
    """
    für Gas. Code vom EIC, https://www.entsog.eu/data/data-portal/codes-list
    """
    zaehlwerke_der_beteiligten_marktrolle: Optional[list["Zaehlwerk"]] = Field(
        default=None, alias="zaehlwerkeDerBeteiligtenMarktrolle", title="Zaehlwerkederbeteiligtenmarktrolle"
    )
    """
    Lokationszuordnung, um bspw. die zugehörigen Messlokationen anzugeben
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    messtechnische_einordnung: MesstechnischeEinordnung = Field(..., alias="messtechnischeEinordnung")
    uebertragungsnetzgebiet: Optional[Regelzone] = None
    variant: Variant
    community_id: str = Field(..., alias="communityId", title="Communityid")
    prognose_grundlage: Optional[Prognosegrundlage] = Field(default=None, alias="prognoseGrundlage")
    prognose_grundlage_detail: Optional[Profiltyp] = Field(default=None, alias="prognoseGrundlageDetail")
