from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.ablesende_rolle import AblesendeRolle
from ..enum.ablesungsstatus import Ablesungsstatus
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.messwertstatus import Messwertstatus
from ..enum.wertermittlungsverfahren import Wertermittlungsverfahren

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut


class Verbrauch(BaseModel):
    """
    Abbildung eines zeitlich abgegrenzten Verbrauchs

    .. raw:: html

        <object data="../_static/images/bo4e/com/Verbrauch.svg" type="image/svg+xml"></object>

    .. HINT::
        `Verbrauch JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Verbrauch.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Eine generische ID, die für eigene Zwecke genutzt werden kann.
    Z.B. könnten hier UUIDs aus einer Datenbank stehen oder URLs zu einem Backend-System.
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    einheit: Optional[Mengeneinheit] = None
    """
    Gibt die Einheit zum jeweiligen Wert an
    """
    enddatum: Optional[datetime] = Field(default=None, title="Enddatum")
    """
    Exklusives Ende des Zeitraumes, für den der Verbrauch angegeben wird
    """
    messwertstatus: Optional[Messwertstatus] = None
    obis_kennzahl: str = Field(..., alias="obisKennzahl", title="Obiskennzahl")
    """
    Die OBIS-Kennzahl für den Wert, die festlegt, welche Größe mit dem Stand gemeldet wird, z.B. '1-0:
    """
    startdatum: Optional[datetime] = Field(default=None, title="Startdatum")
    """
    Inklusiver Beginn des Zeitraumes, für den der Verbrauch angegeben wird
    """
    wert: Decimal = Field(..., title="Wert")
    """
    Gibt den absoluten Wert der Menge an
    """
    wertermittlungsverfahren: Optional[Wertermittlungsverfahren] = None
    """
    Gibt an, ob es sich um eine PROGNOSE oder eine MESSUNG handelt
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    ablesegrund: Optional[str] = Field(default=None, title="Ablesegrund")
    ablesebeschreibung: Optional[str] = Field(default=None, title="Ablesebeschreibung")
    periodenverbrauch: Optional[Decimal] = Field(default=None, title="Periodenverbrauch")
    periodenverbrauch_ursprung: Optional[str] = Field(
        default=None, alias="periodenverbrauchUrsprung", title="Periodenverbrauchursprung"
    )
    ableser: Optional[AblesendeRolle] = None
    status: Optional[Ablesungsstatus] = None
    energiegehalt_gas: Optional[Decimal] = Field(default=None, alias="energiegehaltGas", title="Energiegehaltgas")
    energiegehalt_gas_gueltig_von: Optional[datetime] = Field(
        default=None, alias="energiegehaltGasGueltigVon", title="Energiegehaltgasgueltigvon"
    )
    energiegehalt_gas_gueltig_bis: Optional[datetime] = Field(
        default=None, alias="energiegehaltGasGueltigBis", title="Energiegehaltgasgueltigbis"
    )
    umwandlungsfaktor_gas: Optional[Decimal] = Field(
        default=None, alias="umwandlungsfaktorGas", title="Umwandlungsfaktorgas"
    )
    umwandlungsfaktor_gas_gueltig_von: Optional[datetime] = Field(
        default=None, alias="umwandlungsfaktorGasGueltigVon", title="Umwandlungsfaktorgasgueltigvon"
    )
    umwandlungsfaktor_gas_gueltig_bis: Optional[datetime] = Field(
        default=None, alias="umwandlungsfaktorGasGueltigBis", title="Umwandlungsfaktorgasgueltigbis"
    )
