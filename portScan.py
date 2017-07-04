import socket
import subprocess
import os
import multiprocessing
import sys
    
class scanport:
    """Attempt to connect to a port on a host to see if it is open
    :param host: Host IP to scan
    :param port: Port to scan
    """

    
    def __init__(self, host, ports, timeout):
        self.openPorts = []
        self.host=host
        self.ports=ports
        self.timeout=timeout

    def scan(self, host, port, timeout):
        s = socket.socket()
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            s.getsockname()
        except socket.error:
            s.close()
            scan = "Port: %s - Closed" % str(port)
            return scan
        s.close()
        scan = "Port: %s - Open" % str(port)
        return scan
    
    def startScan(self):
        for i in range(0, len(self.ports)):
            self.openPorts.append(self.scan(self.host, self.ports[i], self.timeout))

        print self.openPorts

    """def multiPort(host, port, a, b, scan):
    #Attempt to connect to a port on a host to see if it is open
    #:param host: Host IP to scan
    #:param port: Port to scan
        openPort = []
        for port in range(a, b):     
            s = socket.socket()
            s.settimeout(0.05)
            try:
                s.connect((host, port))
            except socket.error:
                s.close()
                continue
            print "Port:   "+str(port)+"\t\t"+" Open"
            openPort.append("Port: "+str(port)+" Open")
            s.close()
        qu.put(openPort)
        return 0

    if port == 0:
        jobs = []; scan = []
        a = 1; b = 400
        qu = multiprocessing.Queue()
        for i in range(1, 4):
            p = multiprocessing.Process(target=multiPort, args=(host, port, a, b,scan,))
            jobs.append(p)
            p.start()
            a = a + 400
            b = b + 400
        p.join()
        while not qu.empty():
            scan.append(qu.get())
    #scan = multiPort(host, port)
    else:"""
            

def getPing(host):
    #obtains average ping to host
    #Used to calculate timeout of portscan.
    print "Testing ping of host for timeout."
    p = subprocess.Popen(['ping', '-q', '-c', '1', host], stdout=subprocess.PIPE)
    ret=p.communicate()

    try:
        averages=ret[0].split(' ')
        averages=averages[-2]
    except:
        print "Error with target IP."
        sys.exit('Exiting Program.')
        
    maxx=averages.split('/')
    maxx=maxx[-2]
    return maxx

def singleScan(host, timeout):
    #port=int(raw_input("Enter port number you would like to scan: "))
    ports=[80, 25, 22]
    sp=scanport(host, ports, timeout)
    sp.startScan()
    
def start():
    
    host=raw_input("Enter target IP: ")
    #Add IP check code here

    
    print "Select a function: single defined ports [s], common ports [c], all ports [a]."
    while True:
        function=raw_input("Which function would you like [s/c/a]: ")
        if function.lower() in ['s', 'c', 'a']:
            break
        else:
            print 'Invalid input!'
            continue

    if function == 's': function='single'
    elif function == 'c': function='common'
    elif function == 'a': function='all'

    print ('Host: %s\t\tScan type: %s' % (host, function))
    while True:
        correct=raw_input("Is this correct [y/n]? ")
        if correct.lower() == 'y':
            break
        elif correct.lower() == 'n':
            whatDo=raw_input("Enter 'q' to quit or 'r' to restart: ")
            if whatDo.lower() =='q':
                sys.exit('Exiting program.')
            elif whatDo.lower() == 'r':
                start()
            else:
                sys.exit('Invalid input, exiting program.')

    timeout=float(getPing(host))*1.5
    print "Timeout found: %s" % str(timeout)
    
    if function == 'single':
        singleScan(host, timeout)
    elif function == 'common':
        commonScan(host, timeout)
    elif function == 'all':
        allScan(host, timeout)
 
    
start()