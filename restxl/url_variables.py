"""    
Default Header objects
"""
from validators import *

class RequiredURLVariableException(Exception):
    def __init__(self,errormsg=''):
        return errormsg

class URLVariableValidationException(Exception):
    def __init__(self,errormsg=''):
        return errormsg

class URLVariable(object):
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
    
class CharVariable(URLVariable):
    def __init__(
        self,max_length=None,min_length=None,
        *args, **kwargs
        ):
        self.max_length = max_length
        self.min_length = min_length
        super(CharVariable, self).__init__(*args, **kwargs)
        
    def validate(self,value):
        if not isinstance(value, str):
            raise URLVariableValidationException
        if self.max_length:
            if len(value) > self.max_length:
                raise URLVariableValidationException(
                    'Value exceeds max length. '
                    'Max length %s. Current length %s'\
                    % (self.max_length,len(value)))
        if self.min_length:
            if len(value) < self.min_length:
                raise URLVariableValidationException(
                    'Value is below min length. '
                    'Min length %s. Current length %s'\
                    % (self.mix_length,len(value)))
        
class IntegerVariable(URLVariable):
    def __init__(
        self,max_value=None,min_value=None,
        *args, **kwargs
        ):
        self.max_value = max_value
        self.min_value = min_value
        super(IntegerVariable, self).__init__(*args, **kwargs)
        
    def validate(self,value):
        if not isinstance(value, int):
            raise URLVariableValidationException(
                'This field requires an integer'
                )
        if self.max_value:
            if value > self.max_value:
                raise URLVariableValidationException(
                    'Value exceeds max value. '
                    'Max value %s. Current value %s'\
                    % (self.max_value,len(value)))
        if self.min_value:
            if value < self.min_value:
                raise URLVariableValidationException(
                    'Value is below min length. '
                    'Min value %s. Current value %s'\
                    % (self.mix_value,len(value)))