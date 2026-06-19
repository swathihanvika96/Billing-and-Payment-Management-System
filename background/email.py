import logging

logger = logging.getLogger(__name__)


def send_payment_email(invoice_id: int):

    logger.info(
        f"Payment successful for Invoice {invoice_id}"
    )

    print(
        f"Payment receipt sent for Invoice {invoice_id}"
    )