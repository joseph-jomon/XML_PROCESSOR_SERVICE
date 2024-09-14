To add **TLS** support (for FTPS) to your current `ftp_handler.py`, you'll use `pyftpdlib`'s `TLS_FTPHandler` to handle encrypted connections. This requires a **TLS/SSL certificate** and some modifications to the FTP server configuration.

Here's how to add TLS support:

### **Step 1: Obtain a TLS Certificate**
- For production, use a **Let's Encrypt** certificate. You can generate a certificate using the following command on your server:
  ```bash
  sudo apt-get install certbot
  sudo certbot certonly --standalone -d your-domain.com
  ```
  The certificate and key will typically be saved in `/etc/letsencrypt/live/your-domain.com/`.

- For testing or development, you can create a **self-signed certificate**:
  ```bash
  openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
  ```
  This command generates `cert.pem` and `key.pem` files in the current directory.

### **Step 2: Modify `ftp_handler.py` to Use `TLS_FTPHandler`**
Here’s how to modify your script to use `TLS_FTPHandler` for FTPS:

1. Import `TLS_FTPHandler`.
2. Set up the certificate and key file paths.
3. Add TLS settings to require secure connections.

### **Updated `ftp_handler.py`**
```python
import os
import zipfile
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
from pyftpdlib.servers import FTPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.xml_validator import validate_xml
from app.xml_parser import parse_xml_to_dataframe

UPLOAD_DIR = "./uploads"

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
        # Extract anbieternummer and Kontingent (placeholder)
        anbieternummer, kontingent = self.extract_metadata(xml_file_path)

        # Validate anbieternummer and kontingent
        if not self.validate_provider(anbieternummer):
            print(f"Invalid anbieternummer: {anbieternummer}")
            os.remove(xml_file_path)
            return

        if not self.check_quota(anbieternummer, kontingent):
            print(f"Quota exceeded for anbieternummer: {anbieternummer}")
            os.remove(xml_file_path)
            return

        # Validate the XML file
        if validate_xml(xml_file_path):
            df = parse_xml_to_dataframe(xml_file_path)
            print(f"Processed DataFrame:\n{df.head()}")
        else:
            print(f"Invalid XML file: {xml_file_path}")

    def extract_metadata(self, xml_file_path):
        # Placeholder function to extract anbieternummer and Kontingent
        anbieternummer = "sample_number"
        kontingent = 100
        return anbieternummer, kontingent

    def validate_provider(self, anbieternummer):
        valid_providers = ["valid_number1", "valid_number2"]
        return anbieternummer in valid_providers

    def check_quota(self, anbieternummer, kontingent):
        current_usage = 50  # Example usage count
        return current_usage < kontingent

def start_ftp_server():
    # Step 1: Create an authorizer to handle user authentication
    authorizer = DummyAuthorizer()
    authorizer.add_user("user1", "password1", UPLOAD_DIR, perm="elradfmw")
    authorizer.add_user("user2", "password2", UPLOAD_DIR, perm="elradfmw")
    authorizer.add_user("user3", "password3", UPLOAD_DIR, perm="elradfmw")

    # Step 2: Create a TLS FTP handler and attach the authorizer
    handler = TLS_FTPHandler
    handler.authorizer = authorizer
    handler.passive_ports = range(30000, 30010)

    # Step 3: Configure TLS settings
    handler.certfile = "/path/to/cert.pem"  # Replace with your certificate path
    handler.keyfile = "/path/to/key.pem"    # Replace with your key path
    handler.tls_control_required = True     # Require TLS for the control connection
    handler.tls_data_required = True        # Require TLS for data connections

    # Step 4: Create and start the FTP server
    server = FTPServer(("0.0.0.0", 21), handler)
    print("FTPS server started...")
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
```

### **Explanation of Changes**
1. **TLS Setup**:
   - Changed the FTP handler to `TLS_FTPHandler` to support FTPS (FTP Secure).
   - Added `certfile` and `keyfile` attributes to specify the paths to the certificate and key files.
   - Set `tls_control_required` and `tls_data_required` to `True` to enforce encrypted connections for both the control and data channels.

2. **Certificate Paths**:
   - Update `handler.certfile` and `handler.keyfile` with the correct paths to your certificate and key files.

### **Step 3: Update `docker-compose.yml` to Include Certificates**
If you're using Docker, make sure to mount the certificate files into the container by modifying your `docker-compose.yml`:
```yaml
version: '3'
services:
  ftp:
    build: .
    working_dir: /app
    volumes:
      - ./uploads:/uploads
      - ./app:/app
      - ./schemas:/schemas
      - /path/to/certs:/path/to/certs  # Mount certificate files into the container
    ports:
      - "21:21"
      - "30000-30009:30000-30009"
```
Replace `/path/to/certs` with the directory on your host that contains `cert.pem` and `key.pem`.

### **Step 4: Testing FTPS with FileZilla Client**
1. Open **FileZilla**.
2. For **Host**, use `ftps://your-domain.com` or `ftps://localhost` if testing locally.
3. Use your FTP **username** and **password**.
4. Ensure **Port** is `21`.
5. In **FileZilla**, choose the **FTPS - FTP over TLS** option.
6. Connect and verify that the connection is now encrypted.

### **Notes**
- If using a **self-signed certificate**, you might receive warnings in FTP clients. You’ll need to instruct users to accept the certificate if it is not from a trusted CA (Certificate Authority).
- **Let's Encrypt Certificates**: Recommended for production to provide a trusted, recognized certificate.

### **Summary**
- Changed the FTP handler to `TLS_FTPHandler` to support FTPS.
- Specified paths to the certificate and key files.
- Modified Docker to mount the certificate files into the container.
- Enforced TLS for both the control and data channels to secure file transfers.

With these changes, your FTP server will now support **FTPS**, encrypting the connection and making file transfers more secure.