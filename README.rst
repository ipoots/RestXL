=====================================
RestXL (python REST framework)
=====================================

This project exists to make it easier to create REST clients that are also
very easy to understand. 

The cores of this project are requests, url variables, headers, and RestXLers.

Simple Example
==============
Example Request

http://api.example.com/API/search?search_term=ipoots

HEADERS::
GET /API/search?search_term=ipoots HTTP/1.1
Host: api.example.com
Auth-User: brian
Auth-Key: abcdefg123456abcdefg123456


Requests
~~~~~~~~
The request to the REST api. This is symbolized below by the Request class

URL Variables
~~~~~~~~~~~~~
Query string variables.  (search term is the specified url variables in the example above)

Headers
~~~~~~~
Request headers.  (auth_user and auth_key are the specified headers in the example above)

These are specified in the following way::

	from restxl import request,client
	
	class KeywordSearch(request.Request):
	   #This is the URL Variable. CharVarible is a subclass of the URLVariable class.
	   search_term = request.CharVariable(required=True)
	    
	   #These are the Headers. CharHeader is a subclass of the Header class.
	   auth_user = request.CharHeader(required=True,verbose_name='Auth-User')
	   auth_key = request.CharHeader(required=True,verbose_name='Auth-Key')
	   
	   class Meta:
	       method = 'GET' #GET is the default
	       response_type = 'xml' #xml is the default
	       request_url = http://www.example.com
	       request_path = '/API/search'
	       
	class ExampleAPI(RestXLer):
	    
	    keyword_search = KeywordSearch
	    
	#To create an instance and use the ExampleAPI do the following
	exapi = ExampleAPI()
	
	#Call the keyword_search method
	key_search = exapi(
	    'keyword_search',
	    search_term='iPoots',
	    auth_user='brian',
	    auth_key='abcdefg123456abcdefg123456'
	    )

    
RestXLer
~~~~~~~~
This is the master client class. Create an attribute for each Request class 
associated with the API. (ExampleAPI is the specified RestXLer in the example above)


Installation
============

Dependencies
~~~~~~~~~~~~

 * simplexmlapi
 * beautifulsoup
 * simplejson or json
 * httplib2

Projects Using RestXL
=====================

 * CloudStory (http://github.com/bjinwright/cloudstory)
    
