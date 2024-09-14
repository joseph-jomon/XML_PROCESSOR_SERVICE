Yes, your **inbound rules** are correctly configured. By allowing **port 21** and the **range 30000-30009** for **TCP** traffic and specifying the source as **all IPv4** and **all IPv6** (`0.0.0.0/0` and `::/0`), you have correctly set up the necessary inbound traffic for the FTP service.

### **What About Outbound Rules?**
For an FTP server, the default outbound rules are typically sufficient. Most FTP server setups do not require special outbound rules beyond the default "allow all" because:

1. **Outbound Data Connections**: The FTP server does not usually initiate outbound connections; it listens for connections from clients.
2. **Responses**: The server’s responses to incoming client requests (on port 21 and passive ports) are generally handled automatically by the stateful nature of firewalls.

### **Default Outbound Rules on DigitalOcean Firewalls**
By default, DigitalOcean firewall outbound rules allow all outgoing traffic. This is generally sufficient for most use cases, including running an FTP server. However, you can specify explicit outbound rules if needed.

### **Explicit Outbound Rules (Optional)**
If you want to explicitly define outbound rules for security purposes, you can do the following:
- **Allow All Outbound Traffic** (default):
  - **Protocol**: TCP
  - **Port Range**: `0-65535`
  - **Destination**: `0.0.0.0/0`, `::/0` (all IPs)

### **Example of Outbound Rules in DigitalOcean Firewall**
1. **Rule 1**: 
   - **Type**: Custom
   - **Protocol**: TCP
   - **Port Range**: `0-65535`
   - **Destination**: `0.0.0.0/0` (all IPv4), `::/0` (all IPv6)

This setup allows your server to initiate connections on any port to any IP address, which is the usual requirement for an FTP server responding to various client requests.

### **Summary:**
- Your **inbound rules** are correctly set for FTP.
- **Outbound rules** can generally be left as "allow all" (the default). If you want explicit control, add a rule to allow all outbound traffic on TCP.
- **No further changes** are required for the outbound rules unless you have specific security restrictions in mind.

This configuration will allow your FTP server to handle both command (port 21) and data (passive port range) connections smoothly.