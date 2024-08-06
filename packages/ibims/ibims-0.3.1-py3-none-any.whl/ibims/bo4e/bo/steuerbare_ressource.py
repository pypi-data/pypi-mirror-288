from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.marktrolle import Marktrolle
from ..enum.steuerkanal_leistungsbeschreibung import SteuerkanalLeistungsbeschreibung
from ..enum.typ import Typ

if TYPE_CHECKING:
    from ..com.konfigurationsprodukt import Konfigurationsprodukt
    from ..zusatz_attribut import ZusatzAttribut
    from .lokationszuordnung import Lokationszuordnung


class SteuerbareRessource(BaseModel):
    """
    Object containing information about a steuerbare Ressource

    .. raw:: html

        <object data="../_static/images/bo4e/bo/SteuerbareRessource.svg" type="image/svg+xml"></object>

    .. HINT::
        `SteuerbareRessource JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/SteuerbareRessource.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.STEUERBARERESSOURCE, alias="_typ")
    """
    Id der steuerbaren Ressource
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    eigenschaft_msb_lokation: Optional[Marktrolle] = Field(default=None, alias="eigenschaftMsbLokation")
    """
    Eigenschaft des Messstellenbetreibers an der Lokation
    """
    konfigurationsprodukte: Optional[list["Konfigurationsprodukt"]] = Field(
        default=None, title="Konfigurationsprodukte"
    )
    """
    Produkt-Daten der Steuerbaren Ressource
    """
    lokationsbuendel_objektcode: Optional[str] = Field(
        default=None, alias="lokationsbuendelObjektcode", title="Lokationsbuendelobjektcode"
    )
    """
    Lokationsbuendel Code, der die Funktion dieses BOs an der Lokationsbuendelstruktur beschreibt.
    """
    lokationszuordnungen: Optional[list["Lokationszuordnung"]] = Field(default=None, title="Lokationszuordnungen")
    """
    Lokationszuordnung, um bspw. die zugehörigen Messlokationen anzugeben
    """
    steuerbare_ressource_id: Optional[str] = Field(
        default=None, alias="steuerbareRessourceId", title="Steuerbareressourceid"
    )
    """
    Id der steuerbaren Ressource
    """
    steuerkanal_leistungsbeschreibung: Optional[SteuerkanalLeistungsbeschreibung] = Field(
        default=None, alias="steuerkanalLeistungsbeschreibung"
    )
    """
    Leistungsbeschreibung des Steuerkanals
    """
    zugeordnete_msb_codenummer: Optional[str] = Field(
        default=None, alias="zugeordneteMsbCodenummer", title="Zugeordnetemsbcodenummer"
    )
    """
    Angabe des Messstellenbetreibers, der der Steuerbaren Ressource zugeordnet ist.
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
