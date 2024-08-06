from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.aggregationsverantwortung import Aggregationsverantwortung
from ..enum.profiltyp import Profiltyp
from ..enum.prognosegrundlage import Prognosegrundlage
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.lastprofil import Lastprofil
    from ..zusatz_attribut import ZusatzAttribut


class Bilanzierung(BaseModel):
    """
    Bilanzierung is a business object used for balancing. This object is no BO4E standard and a complete go
    implementation can be found at
    https://github.com/Hochfrequenz/go-bo4e/blob/3414a1eac741542628df796d6beb43eaa27b0b3e/bo/bilanzierung.go
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    typ: Typ = Field(default=Typ.BILANZIERUNG, alias="_typ", title=" Typ")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="ZusatzAttribute"
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    bilanzierungsbeginn: datetime = Field(..., title="Bilanzierungsbeginn")
    bilanzierungsende: datetime = Field(..., title="Bilanzierungsende")
    bilanzkreis: Optional[str] = Field(default=None, title="Bilanzkreis")
    aggregationsverantwortung: Optional[Aggregationsverantwortung] = None
    lastprofile: Optional[list["Lastprofil"]] = Field(default=None, title="Lastprofile")
    prognosegrundlage: Optional[Prognosegrundlage] = None
    details_prognosegrundlage: Optional[Profiltyp] = Field(default=None, alias="detailsPrognosegrundlage")
    lastprofil_namen: Optional[list[str]] = Field(default=None, alias="lastprofilNamen")
