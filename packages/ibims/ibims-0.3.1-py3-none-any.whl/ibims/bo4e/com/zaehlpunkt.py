from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.mengeneinheit import Mengeneinheit


class Zaehlpunkt(BaseModel):
    """
    The zaehlpunkt object was created during a migration project.
    It contains attributes needed for metering mapping.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    periodenverbrauch_vorhersage: Decimal = Field(
        ..., alias="periodenverbrauchVorhersage", title="Periodenverbrauchvorhersage"
    )
    einheit_vorhersage: Mengeneinheit = Field(default=Mengeneinheit.KWH, alias="einheitVorhersage")
    zeitreihentyp: str = Field(default="Z21", title="Zeitreihentyp")
    kunden_wert: Optional[Decimal] = Field(..., alias="kundenWert", title="Kundenwert")
    einheit_kunde: Optional[Mengeneinheit] = Field(default=None, alias="einheitKunde")
    grundzustaendiger: bool = Field(default=True, title="Grundzustaendiger")
