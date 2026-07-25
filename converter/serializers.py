from rest_framework import serializers

from .models import ConversionJob


class ConversionJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionJob
        fields = [
            'id',
            'original_file',
            'original_file_extension',
            'target_format',
            'converted_file',
            'status',
            'error_message',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'converted_file', 'status', 'error_message',
            'created_at', 'updated_at',
        ]