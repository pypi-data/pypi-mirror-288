from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.quantities_status import QuantitiesStatus
from ..enum.sparte import Sparte
from ..enum.typ import Typ


class TransaktionsdatenQuantities(BaseModel):
    """
    This class adds additional data to the transaktionsdaten, which is needed for an energy amount
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    migration_id: Optional[str] = Field(default=None, title="Migration_id")
    typ: Typ = Field(default=Typ.TRANSAKTIONSDATENQUANTITIES, alias="_typ", title=" Typ")
    import_fuer_storno_adhoc: Optional[str] = Field(default=None, title="Import_fuer_storno_adhoc")
    sparte: Optional[Sparte] = Field(default=None, title="Sparte")
    pruefidentifikator: Optional[str] = Field(default=None, title="Pruefidentifikator")
    datenaustauschreferenz: Optional[str] = Field(default=None, title="Datenaustauschreferenz")
    nachrichtendatum: Optional[str] = Field(default=None, title="Nachrichtendatum")
    nachrichten_referenznummer: Optional[str] = Field(default=None, title="Nachrichten_referenznummer")
    absender: Optional[str] = Field(default=None, title="Absender")
    empfaenger: Optional[str] = Field(default=None, title="Empfaenger")
    dokumentennummer: Optional[str] = Field(default=None, title="Dokumentennummer")
    kategorie: Optional[str] = Field(default=None, title="Kategorie")
    nachrichtenfunktion: Optional[str] = Field(default=None, title="Nachrichtenfunktion")
    trans_typ: Optional[str] = Field(default=None, title="TransTyp")
    datumsformat: Optional[str] = Field(default=None, title="Datumsformat")
    status: QuantitiesStatus = Field(default=QuantitiesStatus.VALID, title="Status")
