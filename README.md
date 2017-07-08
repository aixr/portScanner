## Port Scanner - Python

Port scanner written in Python. Uses multiprocessing module to increase speed.

Supports a number of functions:
1. Single/defined port scanning - Scans ports defined by user. 
2. Common ports scan - Scans ~200 of the most popular services.
3. All ports scan - Will scan all ports of target IP/address. (not yet implemented)

How to use:
`git clone https://github.com/aixr/portScanner/`
`cd portScanner/`
`python portScan.py [arguments]`

Run without any arguments and select target IP and mode in the program.
Run with arguments to select IP and functions.
Arguments:
- Must include target IP/address: 
`-t [ip/address]`
- And one of the following:
`-c					Scan all common ports.`
`-s [port] [port,port,...,port] 	Scan defined port(s).`
`-a 	Scan all ports.`

To do:
- Add all ports function
