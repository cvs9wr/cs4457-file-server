import os
class FileReader:

    def __init__(self):
        pass

    def get(self, filepath, cookies):
        '''
        Returns a binary string of the file contents, or None.
        '''
        print("filepath: "+str(filepath))
        
        try: 
            if filepath == b'files/':
                return (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: 50\n'
            +b'Server: cvs9wr\n'
            +b'\n'+b'<html><body><h1>Welcome to my site :)</h1></body> </html>')
            #print("in-function: "+str(filepath)[2:-1])
            path = str(filepath)[2:-1]
            if '.' not in path and not path.endswith('/'):
                return (b'HTTP/1.1 404 Not Found\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: 50\n'
            +b'Server: cvs9wr\n'
            +b'\n'+b'<html><body><h1>file not found</h1></body> </html>')
            
            if os.path.isdir(path):
                return (b'HTTP/1.1 200 OK\n'
                    +b'Content-Type: text/html\n'
                    +b'Content-Length: 50\n'
                    +b'Server: cvs9wr\n'
                    +b'\n'+b'<html><body><h1>'+path.encode()+b'</h1></body> </html>')
            
            requested_file = open(path, 'rb')
        except: 
            return (b'HTTP/1.1 404 Not Found\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: 50\n'
            +b'Server: cvs9wr\n'
            +b'\n'+b'<html><body><h1>file not found</h1></body> </html>')
        
        #print("in-function: "+str(cookies))
        
        file_data = requested_file.read()
        requested_file.close()
        request = b''
        if path.endswith('.png'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: image/png\n'
            +b'Content-Disposition: inline\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Server: cvs9wr\n'
            +b'\n'+file_data)
        elif path.endswith('.jpg'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: image/jpeg\n'
            +b'Content-Disposition: inline\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Server: cvs9wr\n'
            +b'\n'+file_data)
        elif path.endswith('.gif'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: image/gif\n'
            +b'Content-Disposition: inline\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Server: cvs9wr\n'
            +b'\n'+file_data)
        elif path.endswith('.html'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: text/html\n'
            +b'Content-Disposition: inline\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Server: cvs9wr\n'
            +b'\n'+file_data)
        elif path.endswith('.css'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: text/css\n'
            +b'Content-Disposition: inline\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Server: cvs9wr\n'
            +b'\n'+file_data)
        else:
            request = (b'HTTP/1.1 404 Not Found\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: 50\n'
            +b'Server: cvs9wr\n'
            +b'\n'+b'<html><body><h1>file not found</h1></body> </html>')
        return request

    def head(self, filepath, cookies):
        '''
        Returns the size to be returned, or None.
        '''
        try: 
            #print("in-function: "+str(filepath)[2:-1])
            path = str(filepath)[2:-1]
            requested_file = open(path, 'rb')
            val = str.encode(str(os.path.getsize(path)))
            requested_file.close()
        except: 
            return None
        return val
