from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.befestigungsart import Befestigungsart
from ..enum.messwerterfassung import Messwerterfassung
from ..enum.registeranzahl import Registeranzahl
from ..enum.sparte import Sparte
from ..enum.typ import Typ
from ..enum.zaehlerauspraegung import Zaehlerauspraegung
from ..enum.zaehlergroesse import Zaehlergroesse
from ..enum.zaehlertyp import Zaehlertyp
from ..enum.zaehlertyp_spezifikation import ZaehlertypSpezifikation

if TYPE_CHECKING:
    from ..com.zaehlwerk import Zaehlwerk
    from ..com.zeitraum import Zeitraum
    from ..zusatz_attribut import ZusatzAttribut
    from .geraet import Geraet
    from .geschaeftspartner import Geschaeftspartner


class Zaehler(BaseModel):
    """
    Object containing information about a meter/"Zaehler".

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Zaehler.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zaehler JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Zaehler.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.ZAEHLER, alias="_typ")
    """
    Typisierung des Zählers
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    befestigungsart: Optional[Befestigungsart] = None
    """
    Besondere Spezifikation des Zählers
    """
    eichung_bis: Optional[datetime] = Field(default=None, alias="eichungBis", title="Eichungbis")
    """
    Zählerkonstante auf dem Zähler
    """
    geraete: Optional[list["Geraet"]] = Field(default=None, title="Geraete")
    """
    Größe des Zählers
    """
    ist_fernschaltbar: Optional[bool] = Field(default=None, alias="istFernschaltbar", title="Istfernschaltbar")
    """
    Der Hersteller des Zählers
    """
    letzte_eichung: Optional[datetime] = Field(default=None, alias="letzteEichung", title="Letzteeichung")
    """
    Bis zu diesem Datum (exklusiv) ist der Zähler geeicht.
    """
    messwerterfassung: Optional[Messwerterfassung] = Field(default=None, title="Messwerterfassung")
    registeranzahl: Optional[Registeranzahl] = None
    """
    Spezifikation bezüglich unterstützter Tarif
    """
    sparte: Sparte
    """
    Nummerierung des Zählers,vergeben durch den Messstellenbetreiber
    """
    zaehlerauspraegung: Optional[Zaehlerauspraegung] = None
    """
    Strom oder Gas
    """
    zaehlergroesse: Optional[Zaehlergroesse] = None
    """
    Befestigungsart
    """
    zaehlerhersteller: Optional["Geschaeftspartner"] = None
    """
    Der Hersteller des Zählers
    """
    zaehlerkonstante: Optional[Decimal] = Field(default=None, title="Zaehlerkonstante")
    """
    Spezifikation bezüglich unterstützter Tarif
    """
    zaehlernummer: str = Field(..., title="Zaehlernummer")
    """
    Nummerierung des Zählers,vergeben durch den Messstellenbetreiber
    """
    zaehlertyp: Optional[Zaehlertyp] = None
    """
    Spezifikation die Richtung des Zählers betreffend
    """
    zaehlertyp_spezifikation: Optional[ZaehlertypSpezifikation] = Field(default=None, alias="zaehlertypSpezifikation")
    """
    Messwerterfassung des Zählers
    """
    zaehlwerke: list["Zaehlwerk"] = Field(..., title="Zaehlwerke")
    """
    Typisierung des Zählers
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    nachstes_ablesedatum: Optional[datetime] = Field(
        default=None, alias="nachstesAblesedatum", title="Nachstesablesedatum"
    )
    aktiver_zeitraum: Optional["Zeitraum"] = Field(default=None, alias="aktiverZeitraum")
