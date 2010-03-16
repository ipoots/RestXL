"""    
Base Field object
"""
from validators import *
class RequiredFieldException(Exception):
    def __init__(self,errormsg=''):
        return errormsg
class FieldValidationException(Exception):
    def __init__(self,errormsg=''):
        return errormsg
class Field(object):
    """
    Base RestXL field. All field types are subclassed from this class.
    """
    def __init__(
        self,required=False,validators=[]
        ):
        self.required = required
        self.validators = validators
        if self.required:
            self.validators.append(RequiredValidator)
    def validate(self,value):
        for i in self.validators:
            i.validate()
    
class CharField(Field):
    def __init__(
        self,max_length=None,min_length=None,
        *args, **kwargs
        ):
        self.max_length = max_length
        self.min_length = min_length
        super(CharField, self).__init__(*args, **kwargs)
        
    def validate(self,value):
        if not isinstance(value, str):
            raise FieldValidationException
        if self.max_length:
            if len(value) > self.max_length:
                raise FieldValidationException(
                    'Value exceeds max length. '
                    'Max length %s. Current length %s'\
                    % (self.max_length,len(value)))
        if self.min_length:
            if len(value) < self.min_length:
                raise FieldValidationException(
                    'Value is below min length. '
                    'Min length %s. Current length %s'\
                    % (self.mix_length,len(value)))
        
class IntegerField(Field):
    def __init__(
        self,max_value=None,min_value=None,
        *args, **kwargs
        ):
        self.max_value = max_value
        self.min_value = min_value
        super(CharField, self).__init__(*args, **kwargs)
        
    def validate(self,value):
        if not isinstance(value, int):
            raise FieldValidationException(
                'This field requires an integer'
                )
        if self.max_value:
            if value > self.max_value:
                raise FieldValidationException(
                    'Value exceeds max value. '
                    'Max value %s. Current value %s'\
                    % (self.max_value,len(value)))
        if self.min_value:
            if value < self.min_value:
                raise FieldValidationException(
                    'Value is below min length. '
                    'Min value %s. Current value %s'\
                    % (self.mix_value,len(value)))

