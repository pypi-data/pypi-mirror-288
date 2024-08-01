from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.e_mobilitaetsart import EMobilitaetsart
from ..enum.erzeugungsart import Erzeugungsart
from ..enum.speicherart import Speicherart
from ..enum.technische_ressource_nutzung import TechnischeRessourceNutzung
from ..enum.technische_ressource_verbrauchsart import TechnischeRessourceVerbrauchsart
from ..enum.typ import Typ
from ..enum.waermenutzung import Waermenutzung

if TYPE_CHECKING:
    from ..com.menge import Menge
    from ..zusatz_attribut import ZusatzAttribut
    from .lokationszuordnung import Lokationszuordnung


class TechnischeRessource(BaseModel):
    """
    Object containing information about a technische Ressource

    .. raw:: html

        <object data="../_static/images/bo4e/bo/TechnischeRessource.svg" type="image/svg+xml"></object>

    .. HINT::
        `TechnischeRessource JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/bo/TechnischeRessource.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Optional[str] = Field(default=None, alias="_id", title=" Id")
    """
    Hier können IDs anderer Systeme hinterlegt werden (z.B. eine SAP-GP-Nummer oder eine GUID)
    """
    typ: Typ = Field(default=Typ.TECHNISCHERESSOURCE, alias="_typ")
    """
    Identifikationsnummer einer technischen Ressource
    """
    version: str = Field(default="v202401.4.0", alias="_version", title=" Version")
    """
    Version der BO-Struktur aka "fachliche Versionierung"
    """
    emobilitaetsart: Optional[EMobilitaetsart] = None
    """
    Art der E-Mobilität
    """
    erzeugungsart: Optional[Erzeugungsart] = None
    """
    Art der Erzeugung der Energie
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
    nennleistungabgabe: Optional["Menge"] = None
    """
    Nennleistung (Abgabe)
    """
    nennleistungaufnahme: Optional["Menge"] = None
    """
    Nennleistung (Aufnahme)
    """
    speicherart: Optional[Speicherart] = None
    """
    Art des Speichers
    """
    speicherkapazitaet: Optional["Menge"] = None
    """
    Speicherkapazität
    """
    technische_ressource_id: Optional[str] = Field(
        default=None, alias="technischeRessourceId", title="Technischeressourceid"
    )
    """
    Identifikationsnummer einer technischen Ressource
    """
    technische_ressource_nutzung: Optional[TechnischeRessourceNutzung] = Field(
        default=None, alias="technischeRessourceNutzung"
    )
    """
    Art und Nutzung der technischen Ressource
    """
    technische_ressource_verbrauchsart: Optional[TechnischeRessourceVerbrauchsart] = Field(
        default=None, alias="technischeRessourceVerbrauchsart"
    )
    """
    Verbrauchsart der technischen Ressource
    """
    vorgelagerte_messlokation_id: Optional[str] = Field(
        default=None, alias="vorgelagerteMesslokationId", title="Vorgelagertemesslokationid"
    )
    """
    Vorgelagerte Messlokation ID
    """
    waermenutzung: Optional[Waermenutzung] = None
    """
    Wärmenutzung
    """
    zugeordnete_marktlokation_id: Optional[str] = Field(
        default=None, alias="zugeordneteMarktlokationId", title="Zugeordnetemarktlokationid"
    )
    """
    Referenz auf die der technischen Ressource zugeordneten Marktlokation
    """
    zugeordnete_steuerbare_ressource_id: Optional[str] = Field(
        default=None, alias="zugeordneteSteuerbareRessourceId", title="Zugeordnetesteuerbareressourceid"
    )
    """
    Referenz auf die der technischen Ressource zugeordneten Steuerbaren Ressource
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
