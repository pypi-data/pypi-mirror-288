from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.zaehlertyp import Zaehlertyp

if TYPE_CHECKING:
    from ..zusatz_attribut import ZusatzAttribut
    from .adresse import Adresse
    from .menge import Menge
    from .zeitraum import Zeitraum


class Ausschreibungsdetail(BaseModel):
    """
    Die Komponente Ausschreibungsdetail wird verwendet um die Informationen zu einer Abnahmestelle innerhalb eines
    Ausschreibungsloses abzubilden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Ausschreibungsdetail.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ausschreibungsdetail JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/BO4E/BO4E-Schemas/v202401.4.0/src/bo4e_schemas/com/Ausschreibungsdetail.json>`_
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
    ist_lastgang_vorhanden: Optional[bool] = Field(
        default=None, alias="istLastgangVorhanden", title="Istlastgangvorhanden"
    )
    """
    Zeigt an, ob es zu der Marktlokation einen Lastgang gibt.
    Falls ja, kann dieser abgerufen werden und daraus die Verbrauchswerte ermittelt werden
    """
    kunde: Optional[str] = Field(default=None, title="Kunde")
    """
    Bezeichnung des Kunden, der die Marktlokation nutzt
    """
    lieferzeitraum: Optional["Zeitraum"] = None
    """
    Angefragter Zeitraum für die ausgeschriebene Belieferung
    """
    marktlokations_id: Optional[str] = Field(default=None, alias="marktlokationsId", title="Marktlokationsid")
    """
    Identifikation einer ausgeschriebenen Marktlokation
    """
    marktlokationsadresse: Optional["Adresse"] = None
    """
    Die Adresse an der die Marktlokation sich befindet
    """
    marktlokationsbezeichnung: Optional[str] = Field(default=None, title="Marktlokationsbezeichnung")
    """
    Bezeichnung für die Lokation, z.B. 'Zentraler Einkauf, Hamburg'
    """
    netzbetreiber: Optional[str] = Field(default=None, title="Netzbetreiber")
    """
    Bezeichnung des zuständigen Netzbetreibers, z.B. 'Stromnetz Hamburg GmbH'
    """
    netzebene_lieferung: Optional[str] = Field(default=None, alias="netzebeneLieferung", title="Netzebenelieferung")
    """
    In der angegebenen Netzebene wird die Marktlokation versorgt, z.B. MSP für Mittelspannung
    """
    netzebene_messung: Optional[str] = Field(default=None, alias="netzebeneMessung", title="Netzebenemessung")
    """
    In der angegebenen Netzebene wird die Lokation gemessen, z.B. NSP für Niederspannung
    """
    prognose_arbeit_lieferzeitraum: Optional["Menge"] = Field(default=None, alias="prognoseArbeitLieferzeitraum")
    """
    Ein Prognosewert für die Arbeit innerhalb des angefragten Lieferzeitraums der ausgeschriebenen Lokation
    """
    prognose_jahresarbeit: Optional["Menge"] = Field(default=None, alias="prognoseJahresarbeit")
    """
    Prognosewert für die Jahresarbeit der ausgeschriebenen Lokation
    """
    prognose_leistung: Optional["Menge"] = Field(default=None, alias="prognoseLeistung")
    """
    Prognosewert für die abgenommene maximale Leistung der ausgeschriebenen Lokation
    """
    rechnungsadresse: Optional["Adresse"] = None
    """
    Die (evtl. abweichende) Rechnungsadresse
    """
    zaehlernummer: Optional[str] = Field(default=None, title="Zaehlernummer")
    """
    Die Bezeichnung des Zählers an der Marktlokation
    """
    zaehlertechnik: Optional[Zaehlertyp] = None
    """
    Spezifikation, um welche Zählertechnik es sich im vorliegenden Fall handelt, z.B. Leistungsmessung
    """
    zusatz_attribute: Optional[list["ZusatzAttribut"]] = Field(
        default=None, alias="zusatzAttribute", title="Zusatzattribute"
    )
