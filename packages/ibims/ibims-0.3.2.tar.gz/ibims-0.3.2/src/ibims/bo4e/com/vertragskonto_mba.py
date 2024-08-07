from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.kontaktart import Kontaktart

if TYPE_CHECKING:
    from .adresse import Adresse
    from .vertragskonto_cba import VertragskontoCBA


class VertragskontoMBA(BaseModel):
    """
    Models an MBA (master billing account). Its main purpose is to bundle CBAs together having the same address in
    their related contracts. This feature supports a single invoice for all CBAs instead of several
    invoices for each.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    ouid: int = Field(..., title="Ouid")
    vertrags_adresse: "Adresse" = Field(..., alias="vertragsAdresse")
    vertragskontonummer: str = Field(..., title="Vertragskontonummer")
    rechnungsstellung: Kontaktart
    cbas: list["VertragskontoCBA"] = Field(..., title="Cbas")
