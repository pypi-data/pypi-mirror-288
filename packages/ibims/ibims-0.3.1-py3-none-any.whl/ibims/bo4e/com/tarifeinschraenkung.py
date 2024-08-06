from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.voraussetzungen import Voraussetzungen

if TYPE_CHECKING:
    from ..bo.geraet import Geraet
    from ..zusatz_attribut import ZusatzAttribut
    from .menge import Menge


class Tarifeinschraenkung(BaseModel):
    """
    Mit dieser Komponente werden Einschränkungen für die Anwendung von Tarifen modelliert.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifeinschraenkung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifeinschraenkung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Tarifeinschraenkung.json>`_
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
    einschraenkungleistung: Optional[list["Menge"]] = Field(default=None, title="Einschraenkungleistung")
    """
    Die vereinbarte Leistung, die (näherungsweise) abgenommen wird.
    Insbesondere Gastarife können daran gebunden sein, dass die Leistung einer vereinbarten Höhe entspricht.
    """
    einschraenkungzaehler: Optional[list["Geraet"]] = Field(default=None, title="Einschraenkungzaehler")
    """
    Liste der Zähler/Geräte, die erforderlich sind, damit dieser Tarif zur Anwendung gelangen kann.
    (Falls keine Zähler angegeben sind, ist der Tarif nicht an das Vorhandensein bestimmter Zähler gebunden.)
    """
    voraussetzungen: Optional[list[Voraussetzungen]] = Field(default=None, title="Voraussetzungen")
    """
    Voraussetzungen, die erfüllt sein müssen, damit dieser Tarif zur Anwendung kommen kann
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
    zusatzprodukte: Optional[list[str]] = Field(default=None, title="Zusatzprodukte")
    """
    Weitere Produkte, die gemeinsam mit diesem Tarif bestellt werden können
    """
