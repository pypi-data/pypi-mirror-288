from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .sepa_info import SepaInfo


class Bankverbindung(BaseModel):
    """
    This component contains bank connection information.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    iban: Optional[str] = Field(default=None, title="Iban")
    bic: Optional[str] = Field(default=None, title="Bic")
    gueltig_seit: Optional[datetime] = Field(default=None, alias="gueltigSeit", title="Gueltigseit")
    gueltig_bis: Optional[datetime] = Field(default=None, alias="gueltigBis", title="Gueltigbis")
    bankname: Optional[str] = Field(default=None, title="Bankname")
    sepa_info: Optional["SepaInfo"] = Field(default=None, alias="sepaInfo")
    kontoinhaber: Optional[str] = Field(default=None, title="Kontoinhaber")
    ouid: int = Field(..., title="Ouid")
