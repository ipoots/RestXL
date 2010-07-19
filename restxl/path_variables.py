"""    
Default Header objects
"""
from validators import *
__all__ = [
    "CharPathVariable",
    "IntegerPathVariable",
    "PathVariable"
    ]
class RequiredPathVariableException(Exception):
    def __init__(self,msg):
        self.error_msg = msg
        
    def __str__(self):
        return self.error_msg

class PathVariableValidationException(Exception):
    def __init__(self,errormsg=''):
        self.errormsg = errormsg
        
    def __str__(self):
        return self.errormsg

class PathVariable(object):
    """
    Base RestXL URL Variable. All field types are subclassed from this class.
    """
    
    def __init__(
        self,
        required=False,
        validators=[],
        verbose_name=None
        ):
        self.required = required
        self.validators = validators
        if verbose_name:
            self.verbose_name = verbose_name
        if self.required:
            self.validators.append(RequiredValidator)
    def validate(self,value):
        for i in self.validators:
            i.validate()
class CharPathVariable(PathVariable):
    def __init__(
        self,
        position,
        default_value=None,
        max_length=None,
        min_length=None,
        required=False,
        *args, **kwargs
        ):
        self.max_length = max_length
        self.min_length = min_length
        self.required = required
        super(CharPathVariable, self).__init__(*args, **kwargs)
        
    def validate(self,value):
        if self.required and not value:
            raise PathVariableValidationException('This value is required')
        if not isinstance(value, str):
            if not isinstance(value, unicode):
                raise PathVariableValidationException('Value not a string')
        if self.max_length:
            if len(value) > self.max_length:
                raise PathVariableValidationException(
                    'Value exceeds max length. '
                    'Max length %s. Current length %s'\
                    % (self.max_length,len(value)))
        if self.min_length:
            if len(value) < self.min_length:
                raise PathVariableValidationException(
                    'Value is below min length. '
                    'Min length %s. Current length %s'\
                    % (self.mix_length,len(value)))
        
class IntegerPathVariable(PathVariable):
    def __init__(
        self,position,
        default_value=None,
        max_value=None,min_value=None,
        *args, **kwargs
        ):
        self.max_value = max_value
        self.min_value = min_value
        super(IntegerPathVariable, self).__init__(*args, **kwargs)
        
    def validate(self,value):
        if not isinstance(value, int):
            raise PathVariableValidationException(
                'This field requires an integer'
                )
        if self.max_value:
            if value > self.max_value:
                raise PathVariableValidationException(
                    'Value exceeds max value. '
                    'Max value %s. Current value %s'\
                    % (self.max_value,len(value)))
        if self.min_value:
            if value < self.min_value:
                raise PathVariableValidationException(
                    'Value is below min length. '
                    'Min value %s. Current value %s'\
                    % (self.mix_value,len(value)))