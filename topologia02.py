#!/usr/bin/env python
from mininet.cli import CLI

def excercise03(net):
    (h1, h2, h3, h4, _) = net.hosts

    pcap = h1.popen("tcpdump -w ex03-nat.pcap")
    h1.cmd("sed -i 's/nameserver 127.0.0.53/nameserver 8.8.8.8/' /etc/resolv.conf &&\
        systemctl restart systemd-networkd")
    
    print( h1.cmd("ping -c 10 www.google.cl") )

    http_server = h1.popen("python -m http.server 80")
    print("[+] HTTP Server listening on h1")
    
    CLI(net)
    http_server.terminate()
    pcap.terminate()

tests = { 'ex03': excercise03 }