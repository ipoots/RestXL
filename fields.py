"""
Base Field object
"""
class Field(object):
    def __init__(
        self,max_length=None,min_length=None,
        ):
        self.max_length = max_length
        self.min_length = min_length
    def validate(self,value):
        raise NotImplementedError
    