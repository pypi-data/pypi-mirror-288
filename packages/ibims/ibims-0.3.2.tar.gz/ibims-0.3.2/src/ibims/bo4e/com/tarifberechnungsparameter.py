from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.messpreistyp import Messpreistyp
from ..enum.tarifkalkulationsmethode import Tarifkalkulationsmethode

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .preis import Preis
    from .tarifpreis import Tarifpreis


class Tarifberechnungsparameter(BaseModel):
    """
    In dieser Komponente sind die Berechnungsparameter für die Ermittlung der Tarifkosten zusammengefasst.
    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifberechnungsparameter.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifberechnungsparameter JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Tarifberechnungsparameter.json>`_
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
    berechnungsmethode: Optional[Tarifkalkulationsmethode] = None
    """
    Gibt an, wie die Einzelpreise des Tarifes zu verarbeiten sind
    """
    hoechstpreis_ht: Optional["Preis"] = Field(default=None, alias="hoechstpreisHT")
    """
    Höchstpreis für den Durchschnitts-Arbeitspreis HT
    """
    hoechstpreis_nt: Optional["Preis"] = Field(default=None, alias="hoechstpreisNT")
    """
    Höchstpreis für den Durchschnitts-Arbeitspreis NT
    """
    ist_messpreis_in_grundpreis_enthalten: Optional[bool] = Field(
        default=None, alias="istMesspreisInGrundpreisEnthalten", title="Istmesspreisingrundpreisenthalten"
    )
    """
    True, falls der Messpreis im Grundpreis (GP) enthalten ist
    """
    ist_messpreis_zu_beruecksichtigen: Optional[bool] = Field(
        default=None, alias="istMesspreisZuBeruecksichtigen", title="Istmesspreiszuberuecksichtigen"
    )
    """
    True, falls bei der Bildung des Durchschnittspreises für die Höchst- und Mindestpreisbetrachtung der Messpreis mit
    berücksichtigt wird
    """
    kw_inklusive: Optional[Decimal] = Field(default=None, alias="kwInklusive", title="Kwinklusive")
    """
    Im Preis bereits eingeschlossene Leistung (für Gas)
    """
    kw_weitere_mengen: Optional[Decimal] = Field(default=None, alias="kwWeitereMengen", title="Kwweiteremengen")
    """
    Intervall, indem die über "kwInklusive" hinaus abgenommene Leistung kostenpflichtig wird (z.B. je 5 kW 20 EURO)
    """
    messpreistyp: Optional[Messpreistyp] = None
    """
    Typ des Messpreises
    """
    mindestpreis: Optional["Preis"] = None
    """
    Mindestpreis für den Durchschnitts-Arbeitspreis
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    zusatzpreise: Optional[list["Tarifpreis"]] = Field(default=None, title="Zusatzpreise")
    """
    Liste mit zusätzlichen Preisen, beispielsweise Messpreise und/oder Leistungspreise
    """
