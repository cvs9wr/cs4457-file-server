import os
class FileReader:

    def __init__(self):
        pass

    def get(self, filepath, cookies):
        '''
        Returns a binary string of the file contents, or None.
        Python has built in conversion to these things, all we
        have to do is read the data, turn it into simple html
        and then send it back to the user.
        '''
        print("filepath: "+str(filepath))
        
        try: 
            if filepath == b'files/':
                return (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: 50\n'
            +b'Servers: cvs9wr\n'
            +b'\n'+b'<html><body><h1>Welcome to my site :)</h1></body> </html>')
            #print("in-function: "+str(filepath)[2:-1])
            path = str(filepath)[2:-1]
            if '.' not in path and not path.endswith('/'):
                return (b'HTTP/1.1 404 Not Found\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: 50\n'
            +b'Servers: cvs9wr\n'
            +b'\n'+b'<html><body><h1>file not found</h1></body> </html>')
            
            if os.path.isdir(path):
                return (b'HTTP/1.1 200 OK\n'
                    +b'Content-Type: text/html\n'
                    +b'Content-Length: 50\n'
                    +b'Servers: cvs9wr\n'
                    +b'\n'+b'<html><body><h1>'+path.encode()+b'</h1></body> </html>')
            
            requested_file = open(path, 'rb')
        except: 
            return (b'HTTP/1.1 404 Not Found\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: 50\n'
            +b'Servers: cvs9wr\n'
            +b'\n'+b'<html><body><h1>file not found</h1></body> </html>')
        
        #print("in-function: "+str(cookies))
        
        file_data = requested_file.read()
        print("data-size"+str(len(file_data)))
        requested_file.close()
        request = b''
        if path.endswith('.png'):
            request = (b'HTTP/1.1 200 OK\r\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\r\n'
            +b'Content-Type: image/png\r\n'
            +b'Servers: cvs9wr\r\n'
            +b'\r\n'+file_data)
        elif path.endswith('.jpg'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: image/jpeg\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Servers: cvs9wr\n'
            +b'Connection: close\n'
            +b'\n'+file_data+b'\r\n\n')
        elif path.endswith('.gif'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: image/gif\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Servers: cvs9wr\n'
            +b'Connection: close\n'
            +b'\n'+file_data+b'\r\n\n')
        elif path.endswith('.html'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Servers: cvs9wr\n'
            +b'Connection: close\n'
            +b'\n'+file_data+b'\r\n\n')
        elif path.endswith('.css'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: text/css\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Servers: cvs9wr\n'
            +b'Connection: close\n'
            +b'\n'+file_data+b'\r\n\n')
        elif path.endswith('.txt'):
            request = (b'HTTP/1.1 200 OK\n'
            +b'Content-Type: text/plain\n'
            +b'Content-Length: '+str.encode(str(os.path.getsize(path)))+b'\n'
            +b'Servers: cvs9wr\n'
            +b'\n'+file_data+b'\r\n\n')
        else:
            request = (b'HTTP/1.1 404 Not Found\n'
            +b'Content-Type: text/html\n'
            +b'Content-Length: 50\n'
            +b'Servers: cvs9wr\n'
            +b'Connection: close\n'
            +b'\n'+b'<html><body><h1>file not found</h1></body> </html>'+b'\r\n')
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
