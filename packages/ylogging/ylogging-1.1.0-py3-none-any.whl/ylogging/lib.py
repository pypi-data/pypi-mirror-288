from datetime import datetime
from google.cloud import error_reporting, logging
import pytz


def get_gcp_error_reporting_logging_clients(service_name: str):
    error_reporting_client = error_reporting.Client()
    log_name = service_name
    logging_client = logging.Client()
    logger = logging_client.logger(log_name)
    return error_reporting_client, logger


def get_structured_log_msg(
    context: str, message: str, serialized_data: str | None
) -> dict:
    """
    Logs a structured message to the console.
    """
    utc = pytz.UTC
    now = datetime.now(utc)
    log_msg_dict = {
        "context": context,
        "message": message,
        "serialized_data": serialized_data,
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return log_msg_dict
