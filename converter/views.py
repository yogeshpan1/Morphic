from pathlib import Path

from django.core.files import File
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .libreoffice_converter import ConversionError, convert_file
from .models import ConversionJob
from .serializers import ConversionJobSerializer


class ConvertFileView(APIView):
    """
    POST a file + target_format, get back a finished ConversionJob.

    For now this converts synchronously (the request waits for LibreOffice
    to finish). Once this works end-to-end, this is the piece we hand off
    to a Celery task instead.
    """

    parser_classes = [MultiPartParser]

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        target_format = request.data.get('target_format')

        if not uploaded_file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        if not target_format:
            return Response({'error': 'target_format is required, e.g. "pdf".'}, status=status.HTTP_400_BAD_REQUEST)

        file_extension = Path(uploaded_file.name).suffix.lstrip('.').lower()

        job = ConversionJob.objects.create(
            original_file=uploaded_file,
            original_file_extension=file_extension,
            target_format=target_format,
        )

        job.status = ConversionJob.STATUS_PROCESSING
        job.save(update_fields=['status'])

        try:
            input_path = Path(job.original_file.path)
            output_path = convert_file(input_path, target_format)

            with open(output_path, 'rb') as converted:
                job.converted_file.save(output_path.name, File(converted), save=False)

            job.status = ConversionJob.STATUS_DONE
            job.save(update_fields=['status', 'converted_file'])

        except ConversionError as exc:
            job.status = ConversionJob.STATUS_FAILED
            job.error_message = str(exc)
            job.save(update_fields=['status', 'error_message'])

        serializer = ConversionJobSerializer(job, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)