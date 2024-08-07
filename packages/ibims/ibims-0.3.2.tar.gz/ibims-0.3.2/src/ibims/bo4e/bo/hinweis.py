from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from ..enum.hinweis_thema import HinweisThema
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Hinweis(BaseModel):
    """
    Contains specific hints for the handling of contracts and customers.
    Hints are meant to be read and written by agents or customer service employees.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    typ: Typ = Field(default=Typ.HINWEIS, alias="_typ", title=" Typ")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    erstellungsdatum: datetime = Field(..., title="Erstellungsdatum")
    thema: Union[HinweisThema, str] = Field(..., title="Thema")
    nachricht: str = Field(..., title="Nachricht")
