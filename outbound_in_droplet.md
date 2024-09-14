Yes, that is correct. The outbound rule you mentioned (`all TCP`, `port range: all ports`, `destinations: all IPv4 and all IPv6`) means that your server is already configured to allow all outgoing traffic. Therefore, you **do not need to explicitly add any additional outbound rules** for your FTP server.

This rule allows your FTP server to:
- Respond to incoming client requests (e.g., control connections on port 21).
- Send data back to clients through the passive port range (30000-30009).

This is the default and most common configuration for outbound rules in server environments, ensuring that the server can communicate freely with clients and external services as needed. Your current setup is appropriate for running the FTP service.