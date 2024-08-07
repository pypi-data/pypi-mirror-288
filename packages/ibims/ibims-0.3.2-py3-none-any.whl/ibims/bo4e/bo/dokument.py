from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Dokument(BaseModel):
    """
    A generic document reference like for bills, order confirmations and cancellations
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    typ: Typ = Field(default=Typ.DOKUMENT, alias="_typ", title=" Typ")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="ZusatzAttribute"
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    erstellungsdatum: datetime = Field(..., title="Erstellungsdatum")
    has_been_sent: bool = Field(..., alias="hasBeenSent", title="Hasbeensent")
    dokumentenname: str = Field(..., title="Dokumentenname")
    vorlagenname: str = Field(..., title="Vorlagenname")
