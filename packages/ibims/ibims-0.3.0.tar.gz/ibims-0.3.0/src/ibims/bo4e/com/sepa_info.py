from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SepaInfo(BaseModel):
    """
    This class includes details about the sepa mandates.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    sepa_id: str = Field(..., alias="sepaId", title="Sepaid")
    sepa_zahler: bool = Field(..., alias="sepaZahler", title="Sepazahler")
    creditor_identifier: Optional[str] = Field(default=None, alias="creditorIdentifier", title="Creditoridentifier")
    gueltig_seit: Optional[datetime] = Field(default=None, alias="gueltigSeit", title="Gueltigseit")
