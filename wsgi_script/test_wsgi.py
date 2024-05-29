from cgi import parse

HELLO_WORLD = b"Hello World!\n"

def simple_app(environ, start_response):
    status = '200 OK'
    method = environ['REQUEST_METHOD']
    #POST parameters
    if method == 'POST':
        print(environ['wsgi.input'])
    #GET parameters
    if method == 'GET':
        print(environ['QUERY_STRING'])
    
    
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]

application = simple_app