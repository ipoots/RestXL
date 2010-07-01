"""    
Default Header objects
"""
__all__ = [
    "CharHeader",
    "IntegerHeader",
    "Header"
    ]

class RequiredHeaderException(Exception):
    def __init__(self,msg):
        self.error_msg = msg
        
    def __str__(self):
        return self.error_msg
    
class HeaderValidationException(Exception):
    def __init__(self,msg):
        self.error_msg = msg
        
    def __str__(self):
        return self.error_msg
    
class Header(object):
    """
    Base RestXL field. All field types are subclassed from this class.
    """
    def __init__(
        self,
        required=False,
        verbose_name=None,
        validators=[]
        ):
        
        self.required = required
        self.validators = validators
        
        if verbose_name:
            self.verbose_name = verbose_name
    def validate(self,value):
        if self.required and not value:
            raise RequiredHeaderException()
    
class CharHeader(Header):
    def __init__(
        self,max_length=None,min_length=None,
        *args, **kwargs
        ):
        self.max_length = max_length
        self.min_length = min_length
        super(CharHeader, self).__init__(*args, **kwargs)
        
    def validate(self,value):
        if not isinstance(value, str):
            if not isinstance(value, unicode):
                raise HeaderValidationException('Not an instance of a string or unicode')
        if self.max_length:
            if len(value) > self.max_length:
                raise HeaderValidationException(
                    'Value exceeds max length. '
                    'Max length %s. Current length %s'\
                    % (self.max_length,len(value)))
        if self.min_length:
            if len(value) < self.min_length:
                raise HeaderValidationException(
                    'Value is below min length. '
                    'Min length %s. Current length %s'\
                    % (self.mix_length,len(value)))
        
class IntegerHeader(Header):
    def __init__(
        self,max_value=None,min_value=None,
        *args, **kwargs
        ):
        self.max_value = max_value
        self.min_value = min_value
        super(CharHeader, self).__init__(*args, **kwargs)
        
    def validate(self,value):
        if not isinstance(value, int):
            raise HeaderValidationException(
                'This header requires an integer'
                )
        if self.max_value:
            if value > self.max_value:
                raise HeaderValidationException(
                    'Value exceeds max value. '
                    'Max value %s. Current value %s'\
                    % (self.max_value,len(value)))
        if self.min_value:
            if value < self.min_value:
                raise HeaderValidationException(
                    'Value is below min length. '
                    'Min value %s. Current value %s'\
                    % (self.mix_value,len(value)))