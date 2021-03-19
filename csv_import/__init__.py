class ImportTypes:
    """The different csv import types."""

    PRODUCT_ATTRIBUTE = "product_attribute"
    PRODUCT_TYPE = "product_type"
    PRODUCT = "product"
    PRODUCT_VARIANT = "product_variant"
    
    CHOICES = [
        (PRODUCT_ATTRIBUTE, "Product Attribute"),
        (PRODUCT_TYPE, "Product Type"),
        (PRODUCT, "Product"),
        (PRODUCT_VARIANT, "Product Variant"),
    ]


class FileTypes:
    CSV = "csv"

    CHOICES = [
        (CSV, "Plain CSV file.")
    ]

class ImportEvents:
    """The different csv events types."""

    IMPORT_PENDING = "import_pending"
    IMPORT_SUCCESS = "import_success"
    IMPORT_FAILED = "import_failed"
    IMPORT_DELETED = "import_deleted"
    IMPORTED_FILE_SENT = "imported_file_sent"
    IMPORT_FAILED_INFO_SENT = "imported_failed_info_sent"

    CHOICES = [
        (IMPORT_PENDING, "Data import was started."),
        (IMPORT_SUCCESS, "Data import was completed successfully."),
        (IMPORT_FAILED, "Data import failed."),
        (IMPORT_DELETED, "Import file was deleted."),
        (
            IMPORTED_FILE_SENT,
            "Email with import status was sent to the customer.",
        ),
        (
            IMPORT_FAILED_INFO_SENT,
            "Email with info that import failed was sent to the customer.",
        ),
    ]


