To configure the firewall rules on your DigitalOcean droplet for your FTP server, you need to allow traffic on the **FTP control port** (port 21) and the **passive mode data ports** (e.g., 30000–30009). Here’s how to do it:

### **Step 1: Using the DigitalOcean Cloud Firewall**
1. **Log in** to your DigitalOcean account and go to the **Networking** section.
2. Select **Firewalls** from the left menu and either create a new firewall or select an existing one.
3. **Add Inbound Rules**:
   - **Port 21 (Control Port)**:
     - **Protocol**: TCP
     - **Port Range**: 21
     - **Source**: Choose `0.0.0.0/0` (anywhere) if you want to allow connections from any IP, or restrict it to specific IPs if you know the clients' IP addresses.
   - **Passive Mode Ports (e.g., 30000–30009)**:
     - **Protocol**: TCP
     - **Port Range**: 30000-30009
     - **Source**: Same as above (`0.0.0.0/0` for all IPs, or restrict to specific IPs if needed).

4. **Apply the Firewall to Your Droplet**: Ensure that the firewall is applied to your droplet by selecting the droplet from the "Apply to Droplets" section.

### **Step 2: Configuring the Droplet’s Local Firewall (UFW)**
If you have `ufw` (Uncomplicated Firewall) running on your droplet, you need to add similar rules:

1. **Allow Port 21**:
   ```bash
   sudo ufw allow 21/tcp
   ```

2. **Allow Passive Mode Ports**:
   ```bash
   sudo ufw allow 30000:30009/tcp
   ```

3. **Enable UFW** (if not already enabled):
   ```bash
   sudo ufw enable
   ```

4. **Verify UFW Rules**:
   ```bash
   sudo ufw status
   ```

This will list all the currently active firewall rules and ensure that the ports are open.

### **Summary of Ports to Open:**
- **Port 21**: Used for the FTP control connection (sending commands).
- **Passive Mode Port Range (30000-30009)**: Used for data transfer (e.g., file upload/download) in passive mode.

### **Notes:**
- **Passive Mode**: Make sure the passive mode ports defined in your FTP server configuration (`ftp_handler.py`) match the ports opened in the firewall.
- **Security**: For better security, limit the source IP range to known client IPs if possible. Allowing all IPs (`0.0.0.0/0`) is more permissive but may be necessary depending on your use case.

By setting up these firewall rules, you'll allow the necessary traffic for FTP to function correctly on your DigitalOcean droplet.