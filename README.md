# Ddos-TCP-Middlebox-Reflection-Attack  
https://geneva.cs.umd.edu/papers/usenix-weaponizing-ddos.pdf  
Ddos technique with great amplification factor using MiddleBox  

# The technique  
![middle](https://user-images.githubusercontent.com/123097488/222929668-9483378a-52b0-4f28-bf23-448f3ad275fe.png)  

# Reminder: TCP Handshake  
1) SRC sends (SYN)  
2) DEST sends (SYN, ACK)  
3) SRC sends (ACK)  

# Reminder 2: MiddleBox  
MiddleBoxes are state's firewalls, sendind RST and sometimes more(like an entire webpage) to the source who wants to connect to a "forbidden site", and also to the destination. The destination could also send a RST to the Middlebox (infinite loop) 

# The trick  
It may happen that the (SYN,ACK) packet takes another path and don't get through the MiddleBox who have seen the (SYN) packet!  
The trick is to send a SYN packet (SRC:Victim, DST:Filtered site) and ACK packet (SRC:Victim, DEST:Filtered site) just after, to trigger a reply from the MiddleBox(at least a RST, sometimes much more !!!) 

# PoC  

Sending a spoofed SYN packet(SRC=Victim, DST=Pornhub|Youporn|Bittorrent....)  
Sending a spoofed ACK+PSH with a HTTP GET payload packet(SRC=Victim, DST=Pornhub|Youporn|Bittorrent....)  

Don't do anything illegal with that piece of code.  

# Requirements  
You need:
* tcpreplay
* mergecap



