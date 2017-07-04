import socket
import subprocess
import multiprocessing
import sys
import time
    
class scanport:
    
    def __init__(self, host, ports, timeout):
        self.openPorts = []
        self.closedPorts= []
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
            self.closedPorts.append(scan)
            return 0
        s.close()
        scan = "Port: %s - Open" % str(port)
        self.openPorts.append(scan)
        return 0
    
    def startScan(self):
        print "Starting port scan(s)."
        jobs=[]
        t1=time.time()
        if len(self.ports) > 5:
            count=0
            for i in range(0, len(self.ports)):
                p=multiprocessing.Process(target=self.scan, args=(self.host, self.ports[i], self.timeout,))
                jobs.append(p)
                p.start()
                count+=1
                if count >= 4:
                    count=0
                    p.join()
                
            p.join()
        else:
            for i in range(0, len(self.ports)):
                self.scan(self.host, self.ports[i], self.timeout)

        if len(self.openPorts) == 0:
            print "No open ports were found."
        for x in range(0, len(self.openPorts)):
            print self.openPorts[x]
        t2=time.time()
        elapsed=t2-t1
        print "Time elapsed: %s" % str(elapsed)
            

def getPing(host):
    #obtains average ping to host
    #Used to calculate timeout of portscan.
    print "Testing response time of target..."
    p = subprocess.Popen(['ping', '-q', '-c', '10', host], stdout=subprocess.PIPE)
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

def commonScan(host, timeout):
    f=open('commonPorts.txt', 'r')
    common=f.read()
    common=common.replace(' ', '')
    ports=common.split(',')

    for i in range(0, len(ports)):
        try:
            ports[i]=int(ports[i])
        except:
            print "There was an error with the file."
            sys.exit()
    
    sp=scanport(host, ports, timeout)
    sp.startScan()

    
def singleScan(host, timeout):
    
    tmpPorts=raw_input("Enter port(s) you would like to scan: ")
    tmpPorts=tmpPorts.replace(' ', '')
    ports=tmpPorts.split(',')

    for i in range(0, len(ports)):
        try:
            ports[i]=int(ports[i])
        except:
            print "There was an error with something you input. Try again."
            print ports
            singleScan(host, timeout)
            
    sp=scanport(host, ports, timeout)
    sp.startScan()
    
def singleScanArgs(host, timeout, ports):
    
    for i in range(0, len(ports)):
        try:
            ports[i]=int(ports[i])
        except:
            print "There was an error with the ports you input. Try again."
            print ports
            sys.exit()
            
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

    timeout=(float(getPing(host))*2)/1000
    print "Timeout found: %ss" % str(timeout)
    
    if function == 'single':
        singleScan(host, timeout)
    elif function == 'common':
        commonScan(host, timeout)
    elif function == 'all':
        print "Not yet implemented."
        #allScan(host, timeout)

def startArgs():
    if '-t' in sys.argv:
        for i in range(0, len(sys.argv)):
            if sys.argv[i] == '-t':
                try:
                    if sys.argv[i+1][0] != '-':
                        host=sys.argv[i+1]
                    else:
                        sys.exit()
                    
                except:
                    print "Could not find target IP."
                    sys.exit()
                    
    else:
        print "No target IP given."
        sys.exit()
                
    if '-c' in sys.argv:
        timeout=(float(getPing(host))*2)/1000
        commonScan(host, timeout)
    elif '-s' in sys.argv:
        for i in range(0, len(sys.argv)):
            if sys.argv[i]=='-s':
                try:
                    if sys.argv[i+1][0] != '-':
                        ports=sys.argv[i+1]
                    else:
                        sys.exit()
                except:
                    print "Could not find port(s) after -s."
                    sys.exit()
                if ',' in ports:
                    ports=ports.split(',')
                else:
                    port=[]
                    port.append(ports)
                    ports=port
                timeout=(float(getPing(host))*2)/1000
                singleScanArgs(host, timeout, ports)
                
    elif '-a' in sys.argv:
        print "Not yet implemented."
        sys.exit()
    else:
        print "Check arugements given. \nMust have:\n\t-t <target IP>\nAnd one of the following:\n\t-c --Common ports scan.\n\t-s <port> <port,port,...,port> --single/direct ports scan\n\t-a --all ports scan"
        sys.exit()
        

if len(sys.argv) > 0:
    startArgs()
else:
    start()
