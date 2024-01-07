from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os 

def validate_file_extension(value):
    valid_extensions = ['.pdf', '.xlsx', '.csv', '.ppt']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError(_('Unsupported file extension. Allowed extensions are .pdf, .xlsx, .csv, .ppt.'))
