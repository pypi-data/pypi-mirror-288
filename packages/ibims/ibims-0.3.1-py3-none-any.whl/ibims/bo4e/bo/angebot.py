from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.sparte import Sparte
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.angebotsvariante import Angebotsvariante
    from ..zusatz_attribut import ZusatzAttribut
    from .geschaeftspartner import Geschaeftspartner
    from .person import Person


class Angebot(BaseModel):
    """
    Mit diesem BO kann ein Versorgungsangebot zur Strom- oder Gasversorgung oder die Teilnahme an einer Ausschreibung
    übertragen werden. Es können verschiedene Varianten enthalten sein (z.B. ein- und mehrjährige Laufzeit).
    Innerhalb jeder Variante können Teile enthalten sein, die jeweils für eine oder mehrere Marktlokationen erstellt
    werden.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Angebot.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebot JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/Angebot.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.ANGEBOT, alias="_typ")
    """
    Eindeutige Nummer des Angebotes
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    anfragereferenz: Optional[str] = Field(default=None, title="Anfragereferenz")
    """
    Bis zu diesem Zeitpunkt (Tag/Uhrzeit) inklusive gilt das Angebot
    """
    angebotsdatum: Optional[datetime] = Field(default=None, title="Angebotsdatum")
    """
    Erstellungsdatum des Angebots
    """
    angebotsgeber: Optional["Geschaeftspartner"] = None
    """
    Ersteller des Angebots
    """
    angebotsnehmer: Optional["Geschaeftspartner"] = None
    """
    Empfänger des Angebots
    """
    angebotsnummer: Optional[str] = Field(default=None, title="Angebotsnummer")
    """
    Eindeutige Nummer des Angebotes
    """
    bindefrist: Optional[datetime] = Field(default=None, title="Bindefrist")
    """
    Bis zu diesem Zeitpunkt (Tag/Uhrzeit) inklusive gilt das Angebot
    """
    sparte: Optional[Sparte] = None
    """
    Sparte, für die das Angebot abgegeben wird (Strom/Gas)
    """
    unterzeichner_angebotsgeber: Optional["Person"] = Field(default=None, alias="unterzeichnerAngebotsgeber")
    """
    Person, die als Angebotsgeber das Angebots ausgestellt hat
    """
    unterzeichner_angebotsnehmer: Optional["Person"] = Field(default=None, alias="unterzeichnerAngebotsnehmer")
    """
    Person, die als Angebotsnehmer das Angebot angenommen hat
    """
    varianten: Optional[list["Angebotsvariante"]] = Field(default=None, title="Varianten")
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
