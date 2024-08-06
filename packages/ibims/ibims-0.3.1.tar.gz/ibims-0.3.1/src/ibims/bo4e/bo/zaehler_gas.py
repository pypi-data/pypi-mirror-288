from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.messwerterfassung import Messwerterfassung
from ..enum.netzebene import Netzebene
from ..enum.registeranzahl import Registeranzahl
from ..enum.sparte import Sparte
from ..enum.typ import Typ
from ..enum.zaehlerauspraegung import Zaehlerauspraegung
from ..enum.zaehlergroesse import Zaehlergroesse
from ..enum.zaehlertyp import Zaehlertyp

if TYPE_CHECKING:
    from ..com.zaehlwerk import Zaehlwerk
    from ..com.zeitraum import Zeitraum
    from ..zusatz_attribut import ZusatzAttribut
    from .geschaeftspartner import Geschaeftspartner


class ZaehlerGas(BaseModel):
    """
    Resolve some ambiguity of `Strom` and `Gas`
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    typ: Typ = Field(default=Typ.ZAEHLERGAS, alias="_typ", title=" Typ")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="ZusatzAttribute"
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    zaehlernummer: str = Field(..., title="Zaehlernummer")
    sparte: Sparte
    zaehlerauspraegung: Optional[Zaehlerauspraegung] = None
    zaehlertyp: Zaehlertyp
    zaehlwerke: list["Zaehlwerk"] = Field(..., title="Zaehlwerke")
    registeranzahl: Optional[Registeranzahl] = None
    zaehlerkonstante: Optional[Decimal] = Field(default=None, title="Zaehlerkonstante")
    eichung_bis: Optional[datetime] = Field(default=None, alias="eichungBis", title="Eichungbis")
    letzte_eichung: Optional[datetime] = Field(default=None, alias="letzteEichung", title="Letzteeichung")
    zaehlerhersteller: Optional["Geschaeftspartner"] = None
    messwerterfassung: Messwerterfassung
    nachstes_ablesedatum: Optional[datetime] = Field(
        default=None, alias="nachstesAblesedatum", title="Nachstesablesedatum"
    )
    aktiver_zeitraum: Optional["Zeitraum"] = Field(default=None, alias="aktiverZeitraum")
    zaehlergroesse: Zaehlergroesse
    druckniveau: Netzebene
