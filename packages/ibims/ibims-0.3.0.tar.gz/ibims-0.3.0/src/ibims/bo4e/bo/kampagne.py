from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Kampagne(BaseModel):
    """
    A "Kampagne"/campaign models which marketing activities led customers to a product/tariff.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    typ: Typ = Field(default=Typ.KAMPAGNE, alias="_typ", title=" Typ")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="ZusatzAttribute"
    )
    id: str = Field(..., title="Id")
    name: str = Field(..., title="Name")
