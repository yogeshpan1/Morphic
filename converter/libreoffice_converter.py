"""
Wraps the LibreOffice command-line tool to convert office documents
(docx, pptx, xlsx, etc.) into other formats (mainly pdf).

This is the only file that knows about the "soffice" command. Everything
else in the app talks to convert_file() and doesn't care how the
conversion actually happens.
"""

import subprocess

from django.conf import settings


class ConversionError(Exception):
    """Raised when LibreOffice fails to convert a file."""
    pass


def convert_file(input_path, target_format):
    """
    Converts the file at input_path into target_format (e.g. "pdf")
    using LibreOffice headless mode.

    Returns the path to the converted file.
    """
    output_dir = settings.CONVERTED_FILES_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        'soffice',
        '--headless',
        '--convert-to', target_format,
        '--outdir', str(output_dir),
        str(input_path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise ConversionError(
            f'LibreOffice failed (exit code {result.returncode}): {result.stderr}'
        )

    output_filename = input_path.stem + '.' + target_format
    output_path = output_dir / output_filename

    if not output_path.exists():
        raise ConversionError(
            f'Conversion command ran but output file was not found: {output_path}'
        )

    return output_path