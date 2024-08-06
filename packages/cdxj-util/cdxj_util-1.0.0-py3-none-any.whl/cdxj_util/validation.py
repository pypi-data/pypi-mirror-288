from cdxj_util.exceptions import CDXJValidationError
from cdxj_util.utils import is_valid_timestamp

def validate_cdxj_record(record):
    if not isinstance(record, dict):
        raise CDXJValidationError("Record must be a dictionary")
    if "urlkey" not in record or "timestamp" not in record or "metadata" not in record:
        raise CDXJValidationError(
            "Record must contain 'urlkey', 'timestamp', and 'metadata'"
        )
    if not is_valid_timestamp(record["timestamp"]):
        raise CDXJValidationError(f"Invalid timestamp: {record['timestamp']}")
    if not isinstance(record["metadata"], dict):
        raise CDXJValidationError("Metadata must be a dictionary")