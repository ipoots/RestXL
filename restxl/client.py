'''
Created on Jun 25, 2010

@author: brianjinwright
'''
from request import DeclarativeVariablesMetaclass,Request
__all__ = [
    'RestXLer',
    'BaseRestXLer'
    ]
class RestXLerError(Exception):
    def __init__(self,msg):
        self.error_msg = msg
        
    def __str__(self):
        return self.error_msg
    
def get_declared_variables(bases, attrs):
    requests = {}
    r_update = requests.update
    attrs_pop = attrs.pop
    for variable_name, obj in attrs.items():
        if isinstance(obj, DeclarativeVariablesMetaclass):
            r_update({variable_name:attrs_pop(variable_name)})
        
    for base in bases:
        if hasattr(base, 'base_requests'):
            if len(base.base_requests) > 0:
                r_update(base.base_requests)

    return requests

class RequestsDeclarativeVariablesMetaclass(type):
    """
    Partially ripped off from Django's forms.
    http://code.djangoproject.com/browser/django/trunk/django/forms/forms.py
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_requests'] = get_declared_variables(bases, attrs)
        new_class = super(RequestsDeclarativeVariablesMetaclass,
            cls).__new__(cls, name, bases, attrs)

        return new_class


class BaseRestXLer(object):
    """
    Base class for all RestXLer client classes.
    """       
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
                
    def __call__(self,method_name,**kwargs):
        cs = self.base_requests.get(method_name,None)
        if cs:
            req_cls = cs(**kwargs)
            if kwargs.get('request_url',None):
                request_url = kwargs.get('request_url')
                tt = req_cls(request_url)
            else:
                tt = req_cls()
            
        else:
            raise RestXLerError('This method does not exists')
        return tt
        
    
    class Meta:
        """
        This class holds important information about how the request is made.
        """
        method = 'GET'
        response_type = 'xml'
        
class RestXLer(BaseRestXLer):
    __metaclass__ = RequestsDeclarativeVariablesMetaclass
