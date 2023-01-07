from django.core.exceptions import ValidationError

def validate_image_size(value):
    if value.size > 2097152:
        raise ValidationError(
            'You cannot upload file more than 2MB'
        )
    else:
        return value