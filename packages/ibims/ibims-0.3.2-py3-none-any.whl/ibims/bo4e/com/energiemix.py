from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.oekolabel import Oekolabel
from ..enum.oekozertifikat import Oekozertifikat
from ..enum.sparte import Sparte

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .energieherkunft import Energieherkunft


class Energiemix(BaseModel):
    """
    Zusammensetzung der gelieferten Energie aus den verschiedenen Primärenergieformen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Energiemix.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energiemix JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Energiemix.json>`_
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
    anteil: Optional[list["Energieherkunft"]] = Field(default=None, title="Anteil")
    """
    Anteile der jeweiligen Erzeugungsart
    """
    atommuell: Optional[Decimal] = Field(default=None, title="Atommuell")
    """
    Höhe des erzeugten Atommülls in g/kWh
    """
    bemerkung: Optional[str] = Field(default=None, title="Bemerkung")
    """
    Bemerkung zum Energiemix
    """
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    """
    Bezeichnung des Energiemix
    """
    co2_emission: Optional[Decimal] = Field(default=None, alias="co2Emission", title="Co2Emission")
    """
    Höhe des erzeugten CO2-Ausstosses in g/kWh
    """
    energieart: Optional[Sparte] = None
    """
    Strom oder Gas etc.
    """
    energiemixnummer: Optional[int] = Field(default=None, title="Energiemixnummer")
    """
    Eindeutige Nummer zur Identifizierung des Energiemixes
    """
    gueltigkeitsjahr: Optional[int] = Field(default=None, title="Gueltigkeitsjahr")
    """
    Jahr, für das der Energiemix gilt
    """
    ist_in_oeko_top_ten: Optional[bool] = Field(default=None, alias="istInOekoTopTen", title="Istinoekotopten")
    """
    Kennzeichen, ob der Versorger zu den Öko Top Ten gehört
    """
    oekolabel: Optional[list[Oekolabel]] = Field(default=None, title="Oekolabel")
    """
    Ökolabel für den Energiemix
    """
    oekozertifikate: Optional[list[Oekozertifikat]] = Field(default=None, title="Oekozertifikate")
    """
    Zertifikate für den Energiemix
    """
    website: Optional[str] = Field(default=None, title="Website")
    """
    Internetseite, auf der die Strommixdaten veröffentlicht sind
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
