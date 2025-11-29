# PyScan: Multi-Threaded Port Scanner
A fast, lightweight port scanner built in Python.
It uses **threading** to scan multiple ports simultaneously, significantly reducing wait times compared to linear scanning.

## Features
- **Multi-threaded:** Scans 100 ports concurrently.
- **Socket Programming:** Uses raw sockets to establish TCP connections.
- **Clean Output:** specific reporting on open ports only.

## Usage
`python3 scanner.py <target_ip>`
Example: `python3 scanner.py 45.33.32.156`

