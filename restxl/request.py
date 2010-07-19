from url_variables import *
from headers import *
from path_variables import *
import httplib2
from urllib import urlencode
import urllib2
from operator import attrgetter
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
__all__ = [
    'Request',
    'BaseRequest',
    'DynamicRequest'
    'DeclarativeVariablesMetaclass'
    'RestXLResponse'    
    ]
class RestXLRequestError(Exception):
    def __init__(self,msg):
        self.error_msg = msg
        
    def __str__(self):
        return self.error_msg

class RestXLResponse(object):
     def __init__(self,response,content):
         self.response = response
         self.content = content

    
def get_declared_variables(bases, attrs):
    variables = {}
    v_update = variables.update
    headers = {}
    h_update = headers.update
    path_variables = {}
    p_update = path_variables.update
    attrs_pop = attrs.pop
    for variable_name, obj in attrs.items():
        if isinstance(obj, URLVariable):
            v_update({variable_name:attrs_pop(variable_name)})
        if isinstance(obj, Header):
            h_update({variable_name:attrs_pop(variable_name)})
        if isinstance(obj, PathVariable):
            p_update({variable_name:attrs_pop(variable_name)})
        
        
    for base in bases:
        if hasattr(base, 'base_variables'):
            if len(base.base_variables) > 0:
                v_update(base.base_variables)
        if hasattr(base, 'base_headers'):
            if len(base.base_headers) > 0:
                h_update(base.base_headers)
        if hasattr(base, 'base_path_variables'):
            if len(base.base_path_variables) > 0:
                p_update(base.base_path_variables)

    return variables,headers,path_variables

class DeclarativeVariablesMetaclass(type):
    """
    Partially ripped off from Django's forms.
    http://code.djangoproject.com/browser/django/trunk/django/forms/forms.py
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_variables'],attrs['base_headers']\
        ,attrs['base_path_variables'] \
        = get_declared_variables(bases, attrs)
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
        
        
    def __call__(self,request_url=None):
        self._urlvars = {}
        self._headers = {}
        self._pathvars = {}   
        self.load_headers()
        self.load_variables()
        if not request_url:
            request_url = getattr(self.Meta, 'request_url',None)
        request_path = getattr(self.Meta, 'request_path',None)
        if not request_path:
            request_path = self.load_pathvars()
            
        if not request_url:
            raise RestXLRequestError('There is no request_url specified. You must set one.')
        if request_path:
            return self.rest_request(request_url, request_path)
        return self.rest_request(request_url)
    
    def load_headers(self):
        for key,value in self.base_headers.items():
            header = self.kwargs.get(key,None)
            required = getattr(header, 'required',False)
            if required:
                value.validate(header)
            if header != None:
                if hasattr(value, 'verbose_name'):
                    self._headers.update({value.verbose_name:header})
                else:
                    self._headers.update({key:header})
    def load_pathvars(self):
        if len(self.base_path_variables) < 1:
            return None
        pathv_list = list()
        pl_append = pathv_list.append
        for key,value in self.base_path_variables.items():
            pathvar = self.kwargs.get(key,None)
            required = getattr(pathvar, 'required',False)
            if required:
                value.validate(pathvar)
            if pathvar != None:
                setattr(value, 'value', pathvar)
                pl_append(value)
        tt = sorted(pathv_list,key=attrgetter('value'))
        sorted_values = [i.value for i in tt]
        return '/'.join(sorted_values)
    def load_variables(self):
        for key,value in self.base_variables.items():
            urlvar = self.kwargs.get(key,None)
            required = getattr(urlvar, 'required',False)
            if required:
                value.validate(urlvar)
            if urlvar != None:
                if hasattr(value, 'verbose_name'):
                    self._urlvars.update({value.verbose_name:urlvar})
                else:
                    self._urlvars.update({key:urlvar})
                    
    def load_xml(self,content):
        nd = simplexmlapi.loads(content)
        return nd
    
    def load_json(self,content):
        nd = json.loads(content)
        return nd
    
    def load_html(self,content):
        nd = BeautifulSoup(content)
        return nd
    
    def load_raw(self,content):
        return content   
    
    def get_httplib_request(self,request_url,method,body,headers):
        h = httplib2.Http()
        resp, content = h.request(request_url, method=method, body=body,headers=headers)
        return resp, content     
    
    def rest_request(self,request_url,request_path=None):
        
        method = getattr(self.Meta, 'method','GET')
        
        response_type = getattr(self.Meta, 'response_type','xml')
        
        if not request_url:
            raise RestXLRequestError('request_url needs to be defined')
        
        if request_path:
            request_url = '%s/%s'% (request_url,request_path)
            
        else:
            request_url = request_url
        
        if len(self._urlvars) != 0:
            body = urlencode(self._urlvars)
            if method == 'GET': 
                request_url = '%s?%s' %(request_url,body)
                body = None
        else:
            body = None
            
        headers = getattr(self, '_headers',{})
        
        resp,content = self.get_httplib_request(request_url, method, body, headers)
        
        
        if response_type == 'xml':
            nd = self.load_xml(content)
        if response_type == 'json':
            nd = self.load_json(content)
        if response_type == 'html':
            nd = self.load_html(content)
        if response_type == 'raw':
            nd = self.load_raw(content)
        
        return RestXLResponse(resp,nd)

    class Meta:
        """
        This class holds important information about how the request is made.
        """
        method = 'GET'
        response_type = 'xml'
        
class Request(BaseRequest):
    __metaclass__ = DeclarativeVariablesMetaclass 
    