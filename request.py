from fields import Field

def get_declared_fields(bases, attrs, with_base_fields=True):
    fields = {}
    for field_name, obj in attrs.items():
        if isinstance(obj, Field):
            fields.update({field_name:attrs.pop(field_name)})
    for base in bases:
        if hasattr(base, 'base_fields'):
            if len(base.base_fields) > 0:
                fields.update(base.base_fields)
    return fields
class DeclarativeFieldsMetaclass(type):
    """
    Partially ripped off from Django's forms.
    http://code.djangoproject.com/browser/django/trunk/django/forms/forms.py
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_fields'] = get_declared_fields(bases, attrs)
        new_class = super(DeclarativeFieldsMetaclass,
            cls).__new__(cls, name, bases, attrs)

        return new_class
    
class BaseRequest(object):
    def __init__(self,data=None):
        self.data = data or {}
#        self.fields = self.base_fields
    def full_clean(self):
        pass
        
class Request(BaseRequest):
    __metaclass__ = DeclarativeFieldsMetaclass
    
class TestRequest(Request):
    title = Field()
    name = Field()
    
class TestBREquest(TestRequest):
    google = Field()
        