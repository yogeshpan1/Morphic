import uuid

from django.db import models


class ConversionJob(models.Model):
    """
    Tracks a single file conversion request from upload to finished output.
    One row = one file the user wants converted.
    """

    STATUS_QUEUED = 'queued'
    STATUS_PROCESSING = 'processing'
    STATUS_DONE = 'done'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_QUEUED, 'Queued'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_DONE, 'Done'),
        (STATUS_FAILED, 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    original_file = models.FileField(upload_to='uploads/')
    original_file_extension = models.CharField(max_length=10)  # e.g. "docx"

    target_format = models.CharField(max_length=10)  # e.g. "pdf"

    converted_file = models.FileField(upload_to='converted/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} ({self.original_file_extension} -> {self.target_format}, {self.status})'