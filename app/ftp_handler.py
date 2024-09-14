# app/ftp_handler.py

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", "./uploads", perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()

# Start the FTP server in your main service or entry point
if __name__ == "__main__":
    start_ftp_server()
