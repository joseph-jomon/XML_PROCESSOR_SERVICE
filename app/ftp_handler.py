import os
import zipfile
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from xml_validator import validate_xml
from xml_parser import parse_xml_to_dataframe

UPLOAD_DIR = "../uploads"

class FTPFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Ignore directories and handle only files
        if not event.is_directory:
            file_path = event.src_path
            print(f"New file detected: {file_path}")

            # Handle ZIP files and XML files
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(UPLOAD_DIR)
                # Process the extracted XML file(s)
                for f in os.listdir(UPLOAD_DIR):
                    if f.endswith('.xml'):
                        self.process_xml_file(os.path.join(UPLOAD_DIR, f))
            elif file_path.endswith('.xml'):
                self.process_xml_file(file_path)

    def process_xml_file(self, xml_file_path):
        # Validate the XML file
        if validate_xml(xml_file_path):
            # Parse the XML file into a Pandas DataFrame
            df = parse_xml_to_dataframe(xml_file_path)
            print(f"Processed DataFrame:\n{df.head()}")
        else:
            print(f"Invalid XML file: {xml_file_path}")

def start_ftp_server():
    # Step 1: Create an authorizer to handle user authentication
    authorizer = DummyAuthorizer()

    # Step 2: Add multiple users with permissions
    authorizer.add_user("user1", "password1", UPLOAD_DIR, perm="elradfmw")
    authorizer.add_user("user2", "password2", UPLOAD_DIR, perm="elradfmw")
    authorizer.add_user("user3", "password3", UPLOAD_DIR, perm="elradfmw")

    # Step 3: Create an FTP handler and attach the authorizer
    handler = FTPHandler
    handler.authorizer = authorizer
    # Set passive ports range
    handler.passive_ports = range(30000, 30010)  # This should match the range in docker-compose.yml

    # Step 4: Create and start the FTP server
    server = FTPServer(("0.0.0.0", 21), handler)
    print("FTP server started...")
    server.serve_forever()

def start_ftp_file_watcher():
    event_handler = FTPFileHandler()
    observer = Observer()
    observer.schedule(event_handler, UPLOAD_DIR, recursive=True)
    observer.start()
    print("FTP file watcher started.")
    
    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Start the file watcher in a separate thread to allow the FTP server to run concurrently
    from threading import Thread

    # Start FTP server
    ftp_thread = Thread(target=start_ftp_server)
    ftp_thread.start()

    # Start file watcher
    start_ftp_file_watcher()
