from django.db import models
from django.db.models import JSONField  # type: ignore
from django.utils import timezone

from saleor.account.models import User
from saleor.app.models import App
from saleor.core.models import Job
from saleor.core.utils.json_serializer import CustomJsonEncoder

from csv_import import ImportEvents, ImportTypes

class ImportFile(Job):
    user = models.ForeignKey(
        User, related_name="import_files", on_delete=models.CASCADE, null=True
    )
    app = models.ForeignKey(
        App, related_name="import_files", on_delete=models.CASCADE, null=True
    )
    content_file = models.FileField(upload_to="import_files", null=False)
    import_type = models.CharField(max_length=255, choices=ImportTypes.CHOICES)


class ImportEvent(models.Model):
    """Model used to store events that happened during the import file lifecycle."""

    date = models.DateTimeField(default=timezone.now, editable=False)
    type = models.CharField(max_length=255, choices=ImportEvents.CHOICES)
    parameters = JSONField(blank=True, default=dict, encoder=CustomJsonEncoder)
    import_file = models.ForeignKey(
        ImportFile, related_name="import_file_events", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="import_file_events", on_delete=models.CASCADE, null=True
    )
    app = models.ForeignKey(
        App, related_name="import_file_events", on_delete=models.CASCADE, null=True
    )
