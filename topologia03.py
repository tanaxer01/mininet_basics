#!/usr/bin/python3
from mininet.net import Mininet
from mininet.topo import Topo
from time import sleep

class Ex04Topo(Topo):
    "Topology depicted in the first exercise."

    def build(self):
        switches = list()

        chile = self.addHost(f"h1")
        australia = self.addHost(f"h2")

        for n in range(1,5):
            switches.append(self.addSwitch(f"s{n}"))

        self.addLink(chile, switches[0])
        self.addLink(switches[0], switches[1], bw=5, delay='50ms', loss=2)
        self.addLink(switches[1], switches[2], bw=10, delay='72ms', loss=2)
        self.addLink(switches[2], switches[3], bw=5, delay='30ms', loss=2)
        self.addLink(switches[3], australia)

def excercise04(net: Mininet):
    (chile, australia) = net.hosts

    # a) Iperf
    net.iperf((chile, australia), l4Type='UDP', udpBw='31.1Gb')

    # b) FTP Traffic
    australia.cmd('inetutils-inetd')
    sleep(5)
    pcap = chile.popen("tcpdump -w ex04-ftp.pcap")

    ftp_cmd = "user mininet mininet\ncd tarea01\nget un-archivo.png\nquit"
    print( chile.cmd(f"cd /tmp && echo -e '{ftp_cmd}' | ftp -n 10.0.0.2 && echo ENDED") ) 

    # c) HTTP Traffic 
    http_server = australia.popen("python -m http.server 80")

    sleep(5)
    print( chile.cmd(f"wget {australia.IP()}/un-archivo.png ") )
    sleep(5)

    http_server.terminate()
    pcap.terminate()

    
topos = { 'mytopo': Ex04Topo }
tests = { 'ex04': excercise04 }