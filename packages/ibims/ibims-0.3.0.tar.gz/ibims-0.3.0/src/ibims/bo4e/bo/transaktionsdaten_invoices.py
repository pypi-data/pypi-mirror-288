from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enum.invoice_status import InvoiceStatus
from ..enum.sparte import Sparte


class TransaktionsdatenInvoices(BaseModel):
    """
    This class adds additional data to the transaktionsdaten, which is needed for an invoice
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    migration_id: Optional[str] = Field(default=None, title="Migration_id")
    import_fuer_storno_adhoc: Optional[str] = Field(default=None, title="Import_fuer_storno_adhoc")
    sparte: Optional[Sparte] = Field(default=None, title="Sparte")
    pruefidentifikator: Optional[str] = Field(default=None, title="Pruefidentifikator")
    datenaustauschreferenz: Optional[str] = Field(default=None, title="Datenaustauschreferenz")
    nachrichtendatum: Optional[str] = Field(default=None, title="Nachrichtendatum")
    nachrichten_referenznummer: Optional[str] = Field(default=None, title="Nachrichten_referenznummer")
    absender: Optional[str] = Field(default=None, title="Absender")
    empfaenger: Optional[str] = Field(default=None, title="Empfaenger")
    lieferrichtung: Optional[str] = Field(default=None, title="Lieferrichtung")
    referenznummer: Optional[str] = Field(default=None, title="Referenznummer")
    duplikat: Optional[str] = Field(default=None, title="Duplikat")
    status: InvoiceStatus = Field(default=InvoiceStatus.ACCEPTED, title="Status")
