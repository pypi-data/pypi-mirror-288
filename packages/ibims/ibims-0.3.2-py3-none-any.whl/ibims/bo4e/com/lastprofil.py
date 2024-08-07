from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.profiltyp import Profiltyp


class Lastprofil(BaseModel):
    """
    This is not part of the official BO4E standard, but is implemented in the c# and go versions:
    https://github.com/Hochfrequenz/BO4E-dotnet/blob/9bdc151170ddba5c9d7535e863d5a396fe7fec52/BO4E/COM/Lastprofil.cs
    https://github.com/Hochfrequenz/go-bo4e/blob/708b39de0dcea8a9448ed4e7341a2687f6bf7c11/com/lastprofil.go
    Fields, which are not needed for migrations, are omitted and the field "profilart" is modelled as Profiltyp ENUM.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    bezeichnung: Optional[str] = Field(default=None, title="Bezeichnung")
    einspeisung: bool = Field(default=False, title="Einspeisung")
    profilart: Optional[Profiltyp] = None
