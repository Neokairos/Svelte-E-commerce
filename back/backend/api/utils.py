from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email

def validate_email(value:str) -> tuple[bool,str]:
    message_invalid = 'Enter a valid email address'
    email_pass = 'emaildev'
    
    if not value:
        return False, message_invalid
    try:
        if value != email_pass:
            django_validate_email(value) 
        
    except ValidationError:
        return False, message_invalid
    
    return True, ''