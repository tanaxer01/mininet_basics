#!/usr/bin/python3
from mininet.net import Mininet
from mininet.topo import Topo
from math import sqrt, pow
from time import sleep
import re

class Ex01Topo(Topo):
    "Topology depicted in the first exercise."

    def build(self):
        hosts = list()
        switches = list()

        for n in range(1,5):
            hosts.append(self.addHost(f"h{n}"))
            switches.append(self.addSwitch(f"s{n}"))

        # Switch 1
        self.addLink(switches[0], hosts[0])
        self.addLink(switches[0], hosts[1])

        # Switch 2
        self.addLink(switches[1], switches[0])
        self.addLink(switches[1], switches[2], bw=10, delay='15ms')

        # Switch 3
        self.addLink(switches[2], hosts[2])
        self.addLink(switches[2], switches[3], bw=10, delay='30ms', loss=10)

        # Switch 4
        self.addLink(switches[3], hosts[3])

def excercise01(net: Mininet):
    "This function sends 10 icmp packets between hosts to check for connectivity"

    for n, h in enumerate(net.hosts):
        print(f"\t Host {n+1} has IP {h.IP()} and Mac {h.MAC()}")

    # PINGS
    (h1, h2, h3, h4) = net.hosts

    pcap = h1.popen(f"tcpdump -w ex01-pings.pcap icmp")
    # H1 PINGS ----------------------------------------|
    print( h1.cmd(f"ping -c 10 {h2.IP()}") )
    print( h1.cmd(f"ping -c 10 {h3.IP()}") )
    # H3 PINGS ----------------------------------------|
    X = list()
    Ts = [ 2.2622, 2.0930, 2.0452, 2.0227, 2.0096, 2.0010, 1.9949, 1.9905, 1.9870, 1.9842 ]
    for _ in range(10):
        for _ in range(10):
            out = h3.cmd(f"ping -c 10 {h4.IP()}")
            loss = re.search("[0-9]{1,2}(?=% packet loss)",out).group()
            X += [int(loss) / 100]
        
        n = len(X)
        m = sum(X)/n

        s = sqrt( (sum([ pow(i,2) for i in X ]) - n*pow(m,2))/(n-1) )
        sm = s/sqrt(n)    

        t = Ts[n//10 - 1]
        print(f"\t{n//10} -- {m} +- {sm*t}")

    pcap.terminate()

def exercise02(net: Mininet):
    print("[+] Exercise 02: Wget from H2 to H1")
    (h1, h2, h3, h4) = net.hosts

    http_server = h1.popen("python -m http.server 80")
    pcap = h1.popen("tcpdump -w ex02-wget.pcap tcp")

    sleep(5)
    print( h2.cmd(f"wget {h1.IP()} ") )
    sleep(5)

    pcap.terminate()
    http_server.terminate()

topos = { 'mytopo': Ex01Topo }
tests = { 'ex01': excercise01, 'ex02': exercise02 }