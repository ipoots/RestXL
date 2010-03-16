class ValidatorException(Exception):
    def __init__(self,msg):
        return msg
class RequiredValidator(object):
    def __init__(self,value):
        self.value = value
    def validate(self,value):
        if not value:
            raise ValidatorException(
                'This value is required'
                )

class StringValidator(RequiredValidator):
    def validate(self,value):
        if not isinstance(value, str):
            raise ValidatorException(
                'This value should '
                'be a string'
                )

class IntegerValidator(RequiredValidator):
    def validate(self,value):
        if not isinstance(value, int):
            raise ValidatorException(
                'This value should '
                'be a integer'
                )
            
class MaxValueValidator(RequiredValidator):
    def __init__(self,value,compare_value):
        self.value = value
        self.compare_value = compare_value
        
    def validate(self,value):
        if not isinstance(value, int) and self.value > self.compare_value:
            raise ValidatorException(
                'This value should '
                'have a value lesser than '
                '%s. Currently %s' % (self.compare_value, self.value)
                )

class MinValueValidator(MaxValueValidator):
        
    def validate(self,value):
        if not isinstance(value, int) and self.value < self.compare_value:
            raise ValidatorException(
                'This value should '
                'have a value greater than '
                '%s. Currently %s' % (self.compare_value, self.value)
                )

class MaxLengthValidator(RequiredValidator):
    def __init__(self,value,length):
        self.value = value
        self.length = length
        
    def validate(self,value):
        if not isinstance(value, int) and len(self.value) > self.length:
            raise ValidatorException(
                'This value should '
                'have a length lesser than '
                '%s. Currently %s' % (self.length, self.value)
                )

class MinLengthValidator(MaxValueValidator):
        
    def validate(self,value):
        if not isinstance(value, int) and self.value < self.length:
            raise ValidatorException(
                'This value should '
                'have a length greater than '
                '%s. Currently %s' % (self.length, self.value)
                )