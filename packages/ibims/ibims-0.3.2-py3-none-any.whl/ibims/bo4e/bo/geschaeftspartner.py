from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.anrede import Anrede
from ..enum.geschaeftspartnerrolle import Geschaeftspartnerrolle
from ..enum.organisationstyp import Organisationstyp
from ..enum.titel import Titel
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.adresse import Adresse
    from ..com.kontaktweg import Kontaktweg
    from ..zusatz_attribut import ZusatzAttribut
    from .person import Person


class Geschaeftspartner(BaseModel):
    """
    Mit diesem Objekt können Geschäftspartner übertragen werden.
    Sowohl Unternehmen, als auch Privatpersonen können Geschäftspartner sein.
    Hinweis: "Marktteilnehmer" haben ein eigenes BO, welches sich von diesem BO ableitet.
    Hier sollte daher keine Zuordnung zu Marktrollen erfolgen.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Geschaeftspartner.svg" type="image/svg+xml"></object>

    .. HINT::
        `Geschaeftspartner JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Geschaeftspartner.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.GESCHAEFTSPARTNER, alias="_typ")
    """
    Mögliche Anrede der Person
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    adresse: Optional["Adresse"] = None
    """
    Adresse des Geschäftspartners
    """
    amtsgericht: Optional[str] = Field(default=None, title="Amtsgericht")
    """
    Amtsgericht bzw Handelsregistergericht, das die Handelsregisternummer herausgegeben hat
    """
    anrede: Optional[Anrede] = None
    """
    Mögliche Anrede der Person
    """
    ansprechpartner: Optional[list["Person"]] = Field(default=None, title="Ansprechpartner")
    geschaeftspartnerrollen: Optional[list[Geschaeftspartnerrolle]] = Field(
        default=None, title="Geschaeftspartnerrollen"
    )
    """
    Rollen, die die Geschäftspartner inne haben (z.B. Interessent, Kunde)
    """
    glaeubiger_id: Optional[str] = Field(default=None, alias="glaeubigerId", title="Glaeubigerid")
    """
    Die Gläubiger-ID welche im Zahlungsverkehr verwendet wird; Z.B. "DE 47116789"
    """
    handelsregisternummer: Optional[str] = Field(default=None, title="Handelsregisternummer")
    """
    Handelsregisternummer des Geschäftspartners
    """
    individuelle_anrede: Optional[str] = Field(default=None, alias="individuelleAnrede", title="Individuelleanrede")
    kontaktwege: Optional[list["Kontaktweg"]] = Field(default=None, title="Kontaktwege")
    """
    Kontaktwege des Geschäftspartners
    """
    nachname: str = Field(..., title="Nachname")
    """
    Nachname (Familienname) der Person
    """
    organisationsname: Optional[str] = Field(default=None, title="Organisationsname")
    """
    Kontaktwege des Geschäftspartners
    """
    organisationstyp: Optional[Organisationstyp] = None
    titel: Optional[Titel] = None
    """
    Möglicher Titel der Person
    """
    umsatzsteuer_id: Optional[str] = Field(default=None, alias="umsatzsteuerId", title="Umsatzsteuerid")
    """
    Die Steuer-ID des Geschäftspartners; Beispiel: "DE 813281825"
    """
    vorname: Optional[str] = Field(default=None, title="Vorname")
    """
    Vorname der Person
    """
    website: Optional[str] = Field(default=None, title="Website")
    """
    Internetseite des Marktpartners
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    erstellungsdatum: Optional[datetime] = Field(default=None, title="Erstellungsdatum")
    geburtstag: Optional[datetime] = Field(default=None, title="Geburtstag")
    telefonnummer_mobil: Optional[str] = Field(default=None, alias="telefonnummerMobil", title="Telefonnummermobil")
    telefonnummer_privat: Optional[str] = Field(default=None, alias="telefonnummerPrivat", title="Telefonnummerprivat")
    telefonnummer_geschaeft: Optional[str] = Field(
        default=None, alias="telefonnummerGeschaeft", title="Telefonnummergeschaeft"
    )
    firmenname: Optional[str] = Field(default=None, title="Firmenname")
    hausbesitzer: Optional[bool] = Field(default=None, title="Hausbesitzer")
