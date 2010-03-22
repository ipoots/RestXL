from url_variables import *
from headers import *
import httplib2
from urllib import urlencode
import urllib2
try:
    import json
except:
    try:
        import simplejson as json
    except:
        raise ImportError('json or simplejson must be installed')
try:
    import simplexmlapi
except:
    raise ImportError('simplexmlapi must be installed')
try:
    from BeautifulSoup import BeautifulSoup
except:
    raise ImportError('beautifulsoup must be installed')

class RestXLRequestError(Exception):
    def __init__(self,msg):
        return msg
def get_declared_variables(bases, attrs):
    variables = {}
    v_update = variables.update
    headers = {}
    h_update = headers.update
    attrs_pop = attrs.pop
    for variable_name, obj in attrs.items():
        if isinstance(obj, URLVariable):
            v_update({variable_name:attrs_pop(variable_name)})
        if isinstance(obj, Header):
            h_update({variable_name:attrs_pop(variable_name)})
        
    for base in bases:
        if hasattr(base, 'base_variables'):
            if len(base.base_variables) > 0:
                v_update(base.base_variables)
        if hasattr(base, 'base_headers'):
            if len(base.base_headers) > 0:
                h_update(base.base_headers)

    return variables,headers

class DeclarativeVariablesMetaclass(type):
    """
    Partially ripped off from Django's forms.
    http://code.djangoproject.com/browser/django/trunk/django/forms/forms.py
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_variables'],attrs['base_headers'] = get_declared_variables(bases, attrs)
        new_class = super(DeclarativeVariablesMetaclass,
            cls).__new__(cls, name, bases, attrs)

        return new_class


class BaseRequest(object):
    """
    Base class for all RestXL request classes.
    """       
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
                
        
    def __call__(self):
        self._urlvars = {}
        self._headers = {}
        for key,value in self.base_variables.items():
            urlvar = self.kwargs.get(key,None)
            value.validate(urlvar)
            if hasattr(value, 'verbose_name'):
                self._urlvars.update({value.verbose_name:urlvar})
            else:
                self._urlvars.update({key:urlvar})
        for key,value in self.base_headers.items():
            header = self.kwargs.get(key,None)
            value.validate(header)
            if hasattr(value, 'verbose_name'):
                self._headers.update({value.verbose_name:header})
            else:
                self._headers.update({key:header})
        return self.rest_request()
        
    def rest_request(self):
        
        method = getattr(self.Meta, 'method','GET')
         
        response_type = getattr(self.Meta, 'response_type','xml')
        if not hasattr(self.Meta, 'request_url'):
            raise RestXLRequestError('You must have a request url in the Meta class.')
        
        request_url = getattr(self.Meta, 'request_url') + getattr(self.Meta, 'request_path', '')
        if len(self._urlvars) != 0:
            body = urlencode(self._urlvars)
            if method == 'GET':
                request_url.join('?%s' %(body))
                body = None
        else:
            body = None
        headers = getattr(self, '_headers',{})
        h = httplib2.Http()
        resp, content = h.request(request_url, method=method, body=body,headers=headers)
        if response_type == 'xml':
            nd = simplexmlapi.loads(content)
        if response_type == 'json':
            nd = json.loads(content)
        if response_type == 'html':
            nd = BeautifulSoup(content)
        if response_type == 'raw':
            nd = content
        return nd,resp
    
    class Meta:
        """
        This class holds important information about how the request is made.
        """
        method = 'GET'
        response_type = 'xml'
        
class Request(BaseRequest):
    __metaclass__ = DeclarativeVariablesMetaclass
