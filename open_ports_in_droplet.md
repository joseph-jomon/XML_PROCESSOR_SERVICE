The error you encountered, `ECONNREFUSED - Connection refused by server`, indicates that the **data connection** for passive mode could not be established. This usually happens because the server cannot accept incoming connections on the specified passive mode ports. 

In the context of Docker, this issue often arises due to improper port mapping or firewall restrictions. Let's go through the steps to address this problem:

### **1. Ensure Proper Port Mapping in `docker-compose.yml`**

The `docker-compose.yml` file should map the **passive mode ports** correctly. Double-check that your `docker-compose.yml` includes a mapping for the passive mode ports (e.g., `"30000-30009:30000-30009"`). Here's a sample snippet to verify:

```yaml
ftp:
  build: .
  working_dir: /app
  volumes:
    - ./uploads:/uploads  # Directory to store uploaded files
    - ./app:/app  # Mount the application code
    - ./schemas:/schemas  # Mount the XSD schemas
  ports:
    - "21:21"
    - "30000-30009:30000-30009"  # Passive mode ports
```

### **2. Configure Passive Mode Ports in FileZilla Server**

If you haven't already configured the **passive mode** ports in FileZilla Server, you'll need to ensure that it's using the correct range:

1. Open **FileZilla Server Interface**.
2. Go to **Edit** > **Settings**.
3. Under **Passive Mode Settings**:
   - Select **Use custom port range** and enter `30000-30009`.
   - In **External IP address for passive mode transfers**, enter the public IP address of the server if it's hosted remotely (e.g., on a DigitalOcean droplet).

This ensures that FileZilla Server uses the specified range for passive mode and communicates the correct external IP address to clients.

### **3. Check Firewall Settings**

If you are running the FTP server on a cloud server (e.g., DigitalOcean, AWS, etc.), or if your local machine has a firewall, make sure that the following ports are open:
- Port **21**: For FTP command/control.
- Port range **30000-30009**: For passive mode data connections.

#### **On Linux (UFW)**
If using `ufw` (Uncomplicated Firewall) on Linux, run:
```bash
sudo ufw allow 21/tcp
sudo ufw allow 30000:30009/tcp
```

#### **On DigitalOcean or Other Cloud Providers**
Open the necessary ports (21 and the passive mode range) in the firewall settings for your cloud instance.

### **4. Restart Docker Services**
After making changes to `docker-compose.yml` and verifying the firewall settings, restart your Docker services to apply the changes:
```bash
docker-compose down
docker-compose up --build
```

### **5. Retest with FileZilla Client**

- Open FileZilla Client.
- Use the **Host**, **Username**, **Password**, and **Port** as before.
- Click **Quick Connect**.

### **6. Disable "Use EPSV" Mode in FileZilla (Optional)**

If you continue to face issues, you can try disabling the `EPSV` command (extended passive mode) in FileZilla:
1. In FileZilla Client, go to **Edit** > **Settings**.
2. Navigate to **FTP** > **Passive mode**.
3. Uncheck the option **"Use EPSV mode"**.
4. Retest the connection.

### **Summary**
- Make sure the passive mode ports are correctly mapped in the `docker-compose.yml`.
- Configure FileZilla Server to use the correct passive mode port range.
- Open necessary ports in your firewall.
- Restart Docker to apply the changes.

By following these steps, the data connection issue (`ECONNREFUSED`) should be resolved, allowing the FTP client to retrieve the directory listing successfully.