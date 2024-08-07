from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .regionale_gueltigkeit import RegionaleGueltigkeit
    from .sigmoidparameter import Sigmoidparameter


class RegionalePreisstaffel(BaseModel):
    """
    Abbildung einer Preisstaffel mit regionaler Abgrenzung

    .. raw:: html

        <object data="../_static/images/bo4e/com/RegionalePreisstaffel.svg" type="image/svg+xml"></object>

    .. HINT::
        `RegionalePreisstaffel JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/RegionalePreisstaffel.json>`_
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
    einheitspreis: Optional[Decimal] = Field(default=None, title="Einheitspreis")
    """
    Preis pro abgerechneter Mengeneinheit
    """
    regionale_gueltigkeit: Optional["RegionaleGueltigkeit"] = Field(default=None, alias="regionaleGueltigkeit")
    """
    Regionale Eingrenzung der Preisstaffel
    """
    sigmoidparameter: Optional["Sigmoidparameter"] = None
    """
    Parameter zur Berechnung des Preises anhand der Jahresmenge und weiterer netzbezogener Parameter
    """
    staffelgrenze_bis: Optional[Decimal] = Field(default=None, alias="staffelgrenzeBis", title="Staffelgrenzebis")
    """
    Exklusiver oberer Wert, bis zu dem die Staffel gilt
    """
    staffelgrenze_von: Optional[Decimal] = Field(default=None, alias="staffelgrenzeVon", title="Staffelgrenzevon")
    """
    Inklusiver unterer Wert, ab dem die Staffel gilt
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
