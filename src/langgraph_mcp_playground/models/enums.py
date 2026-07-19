from enum import StrEnum


class UploadStatus(StrEnum):
    RECEIVED = "RECEIVED"
    STORED = "STORED"
    PARSING = "PARSING"
    PARSED = "PARSED"
    FAILED = "FAILED"