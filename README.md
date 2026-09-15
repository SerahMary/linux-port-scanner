# Linux Port Scanner

A Python-based network security tool developed in Kali Linux for **remote TCP port scanning** and **local listening-port monitoring**.

The project is designed to help understand computer networking, TCP ports, socket programming, Linux network services, and basic cybersecurity concepts.

---

## Project Overview

The Linux Port Scanner consists of two main components:

1. **Local Port Monitor** - Monitors listening ports on the local Linux system.
2. **Remote Port Scanner** - Scans TCP ports from `1` to `65535` on a specified remote IP address.

The remote scanner displays only ports that are found to be open and attempts to identify the associated service and banner information.

---

## Features

### Local Port Monitor

- Detects listening TCP ports
- Detects listening UDP ports
- Displays local IP addresses and ports
- Identifies protocols
- Identifies common services
- Displays Process ID (PID)
- Displays process names
- Continuously monitors the system
- Detects newly opened ports
- Detects closed ports
- Displays the time when a port change occurs

### Remote Port Scanner

- Accepts a remote IP address as input
- Scans TCP ports from `1` to `65535`
- Uses concurrent scanning for faster execution
- Displays only open ports
- Identifies common services
- Measures response time
- Attempts to retrieve service banners
- Displays version/banner information when available

---

## Project Structure

```text
linux-port-scanner/
│
├── main.py
├── remote_scanner.py
├── README.md
├── .gitignore
└── venv/
```

### File Description

| File | Description |
|------|-------------|
| `main.py` | Local listening-port monitoring tool |
| `remote_scanner.py` | Remote TCP port scanner |
| `README.md` | Project documentation |
| `.gitignore` | Specifies files that Git should ignore |
| `venv/` | Python virtual environment |

> The `venv/` directory is excluded from GitHub using `.gitignore`.

---

## Technologies Used

- **Python 3**
- **Kali Linux**
- **Python Socket Programming**
- **psutil**
- **ThreadPoolExecutor**
- **TCP/IP Networking**
- **Git**
- **GitHub**

---

## Requirements

Before running the project, make sure the following are installed:

- Python 3
- Kali Linux or another Linux-based operating system
- `pip`
- `psutil`

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SerahMary/linux-port-scanner.git
```

### 2. Enter the Project Directory

```bash
cd linux-port-scanner
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate the Virtual Environment

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install psutil
```

---

# Usage

## 1. Local Port Monitor

Run:

```bash
sudo python3 main.py
```

The program monitors the local Linux system and detects listening ports.

The monitor can display information such as:

```text
Port
Protocol
Local Address
Service
PID
Process Name
```

When a new port is detected, it reports:

```text
[+] NEW PORT DETECTED
```

When a previously detected port is no longer listening, it reports:

```text
[-] PORT CLOSED
```

To stop the monitor:

```text
Ctrl + C
```

---

## 2. Remote Port Scanner

Run:

```bash
python3 remote_scanner.py
```

The program asks for the target IP address.

Example:

```text
Enter target IP address: 192.168.1.10
```

The scanner checks TCP ports from:

```text
1 - 65535
```

Only open ports are displayed.

### Example Output

```text
LINUX REMOTE PORT SCANNER

Enter target IP address: 192.168.1.10

OPEN PORTS

Port          : 21
State         : OPEN
Protocol      : TCP
Service       : ftp
Response Time : 151.63 ms
Version/Banner: 220 (vsFTPd 3.0.3)

Port          : 80
State         : OPEN
Protocol      : TCP
Service       : http
Response Time : 172.45 ms
Version/Banner: Server: Apache/2.4.18 (Ubuntu)

Port          : 2222
State         : OPEN
Protocol      : TCP
Service       : Unknown
Response Time : 153.20 ms
Version/Banner: SSH-2.0-OpenSSH_7.2p2 Ubuntu
```

---

# How the Project Works

## Local Port Monitoring

The local monitoring component uses the `psutil` library to retrieve network connections from the Linux system.

It checks which ports are currently listening and stores the results.

During continuous monitoring, the current port list is compared with the previous port list.

If a new port appears:

```text
Current ports > Previous ports
```

the program reports a new port.

If a previously detected port disappears:

```text
Previous ports > Current ports
```

the program reports that the port has been closed.

---

## Remote Port Scanning

The remote scanner uses Python socket connections to test TCP ports.

For each port, the scanner attempts to establish a TCP connection with the target IP address.

If the connection succeeds, the port is considered open.

The scanner then attempts to:

1. Identify the common service associated with the port.
2. Measure the response time.
3. Retrieve a service banner when available.
4. Display the information to the user.

Multiple ports are scanned concurrently using Python's `ThreadPoolExecutor`.

---

# Port States

The scanner primarily focuses on identifying open ports.

### Open

A TCP connection to the target port was successfully established.

### Closed

The target system responded, but the port is not accepting connections.

### Filtered

A firewall or filtering mechanism may prevent the scanner from determining the actual state of the port.

The remote scanner displays **only open ports** in its output.

---

# Service Identification

The scanner attempts to identify services using common TCP port assignments.

Some examples include:

| Port | Common Service |
|------|----------------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |

Service identification is based on standard port assignments and available banner information.

A service running on a non-standard port may therefore appear as `Unknown` even when its banner identifies the actual application.

---

# Banner Detection

Some network services provide information when a connection is established.

This information is known as a **service banner**.

For example:

```text
SSH-2.0-OpenSSH_7.2p2 Ubuntu
```

can indicate that the service is SSH and provide information about the SSH implementation.

HTTP services may provide information such as:

```text
Server: Apache/2.4.18 (Ubuntu)
```

The scanner attempts to retrieve such information when it is available.

However, not every service provides a banner.

---

# Response Time

The remote scanner measures how long it takes to establish a connection to an open port.

The result is displayed in milliseconds.

Example:

```text
Response Time : 151.63 ms
```

Response time can vary depending on:

- Network latency
- Target system load
- Firewall behavior
- Network congestion
- Distance between systems

---

# Concurrency

Scanning all `65535` TCP ports sequentially can take a significant amount of time.

To improve scanning speed, the remote scanner uses multiple worker threads.

The project uses Python's:

```python
ThreadPoolExecutor
```

to perform multiple connection attempts concurrently.

This allows several ports to be tested at the same time.

---

# Learning Objectives

This project helps demonstrate practical concepts related to:

- Computer networking
- TCP/IP
- TCP ports
- Socket programming
- Port scanning
- Network services
- Service identification
- Banner grabbing
- Response-time measurement
- Linux networking
- Python programming
- Python concurrency
- Process monitoring
- Git
- GitHub
- Basic cybersecurity

---

# Use Cases

The project can be used in controlled environments for:

- Cybersecurity learning
- Networking practice
- Python programming practice
- CTF environments
- Personal laboratory environments
- Testing systems that you own
- Authorized security assessments
- Understanding open network services

---

# Limitations

The project has some limitations:

- Remote scanning currently focuses on TCP ports.
- UDP scanning is not currently implemented.
- Some services may not provide banners.
- Banner information may be incomplete or unavailable.
- Service identification may not always be accurate.
- Services running on non-standard ports may appear as `Unknown`.
- Firewalls can affect scanning results.
- Network conditions can affect response times.
- The scanner does not perform advanced vulnerability detection.
- The scanner does not exploit discovered services.

---

# Future Improvements

Possible future improvements include:

- UDP port scanning
- Improved service detection
- Better banner parsing
- Automatic version detection
- Command-line arguments
- Configurable timeout values
- Configurable worker count
- Export results to TXT or CSV
- Generate HTML or PDF reports
- Improved error handling
- Logging
- Scan history
- More detailed network information

---

# Security and Ethical Use

This project is intended for **educational purposes and authorized security testing only**.

Use the scanner only against:

- Systems you own
- Systems in your own laboratory
- CTF machines
- Systems where you have explicit permission to perform security testing

Do not scan systems or networks without authorization.

Unauthorized network scanning may violate organizational policies or applicable laws.

The author is not responsible for misuse of this software.

---

# GitHub

The source code for this project is available on GitHub:

```text
https://github.com/SerahMary/linux-port-scanner
```

---

# Author

**Serah Mary Samuel**

GitHub: `SerahMary`

---

# License

This project currently does not include a specific open-source license.

If the project is later released under an open-source license, the license information will be added here.

---

# Acknowledgement

This project was developed as a practical learning project to explore Python programming, Linux networking, port scanning, and cybersecurity concepts.
