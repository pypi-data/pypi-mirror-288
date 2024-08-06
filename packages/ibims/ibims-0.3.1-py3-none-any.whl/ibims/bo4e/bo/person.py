from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.anrede import Anrede
from ..enum.titel import Titel
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.adresse import Adresse
    from ..com.kontaktweg import Kontaktweg
    from ..com.zustaendigkeit import Zustaendigkeit
    from ..zusatz_attribut import ZusatzAttribut


class Person(BaseModel):
    """
    Object containing information about a Person

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Person.svg" type="image/svg+xml"></object>

    .. HINT::
        `Person JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Person.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.PERSON, alias="_typ")
    """
    Mögliche Anrede der Person
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    adresse: Optional["Adresse"] = None
    """
    Adresse der Person, falls diese von der Adresse des Geschäftspartners abweicht
    """
    anrede: Optional[Anrede] = None
    """
    Mögliche Anrede der Person
    """
    geburtsdatum: Optional[datetime] = Field(default=None, title="Geburtsdatum")
    """
    Geburtsdatum der Person
    """
    individuelle_anrede: Optional[str] = Field(default=None, alias="individuelleAnrede", title="Individuelleanrede")
    kommentar: Optional[str] = Field(default=None, title="Kommentar")
    """
    Weitere Informationen zur Person
    """
    kontaktwege: Optional[list["Kontaktweg"]] = Field(default=None, title="Kontaktwege")
    """
    Kontaktwege der Person
    """
    nachname: Optional[str] = Field(default=None, title="Nachname")
    """
    Nachname (Familienname) der Person
    """
    titel: Optional[Titel] = None
    """
    Möglicher Titel der Person
    """
    vorname: Optional[str] = Field(default=None, title="Vorname")
    """
    Vorname der Person
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    zustaendigkeiten: Optional[list["Zustaendigkeit"]] = Field(default=None, title="Zustaendigkeiten")
    """
    Liste der Abteilungen und Zuständigkeiten der Person
    """
