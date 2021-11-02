# ssh-honeypot

We have implemented an SSH honeypot in this project, which will act as a proxy server for any central server and used to track the behaviour of attacks that are done on any main servers. The function of a honeypot is to represent itself on the internet as a potential target for attackers (usually a server or other high-value asset) and to gather information and notify defenders of any attempts to access the honeypot by unauthorized users.

## Introduction
### How do honeypots work? 
Generally, a honeypot operation consists of a computer, applications, and data that simulate the behavior of a natural system that would be attractive to attackers, such as a financial system, internet of things (IoT) devices, or a public utility or transportation network. It appears as part of a network but is actually isolated and closely monitored. Because there is no reason for legitimate users to access a honeypot, any attempts to communicate with it are considered hostile.
Honeypots may also be put outside the external firewall facing the internet to detect attempts to enter the internal network. The exact placement of the honeypot varies depending on how elaborate it is, the traffic it aims to attract, and how close it is to sensitive resources inside the corporate network. No matter the placement, it will always have some degree of isolation from the production environment. Virtual machines (VMs) are often used to host honeypots. That way, if they are compromised by malware, for example, the honeypot can be quickly restored. Two or more honeypots on a network form a honeynet, while a honey farm is a centralized collection of honeypots and analysis tools.

### What are honeypots used for? 
 - Honeypots are used to capture information from unauthorized intruders that are tricked into accessing them because they appear to be a legitimate part of the network. Security teams deploy these traps as part of their network defense strategy. Honeypots are also used to research the behavior of cyber attackers and the ways they interact with networks.
 - Spam traps are also similar to honeypots. They are email addresses or other network functions set up to attract spam web traffic. Spam traps are used in Project Honey Pot, a web-based network of honeypots embedded in website software. Its purpose is to harvest and collect the Internet Protocol (IP) addresses, email addresses, and related information on spammers so web administrators can minimize the amount of spam on their sites. The group's findings are used for research and law enforcement to combat unsolicited bulk mailing offenses.
 - Honeypots aren't always used as a security measure. Anyone can use them for network surveillance, including hackers. For instance, a Wi-Fi Pineapple lets users create a Wi-Fi honeypot. Wi-Fi Pineapples are relatively cheap because consumer devices make a fake Wi-Fi network that mimics a real one in the vicinity. Unsuspecting individuals mistakenly connect to the artificial Wi-Fi network, and the honeypot operator can then monitor their traffic. 

###

### Technology-Stack 
- Python 
- Paramiko
- Docker

### Contributors🤝 
<table>
<tr align="center">
<td>

Gita Alekhya Paul

<p align="center">
<img src = "https://avatars3.githubusercontent.com/u/54375111?s=460&u=0585ce48d7a98d878ee16041d73695e37b17ade0&v=4"  height="120" alt="Gita Alekhya Paul">
</p>
<p align="center">
<a href = "https://github.com/gitaalekhyapaul"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/gitaalekhyapaul/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>

<td>

Ratanshi Puri

<p align="center">
<img src = "https://avatars.githubusercontent.com/u/51535047?v=4"  height="120" alt="Ratanshi Puri">
</p>
<p align="center">
<a href = "https://github.com/Ratanshi"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/ratanshi/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>

<td>

Nitish Chaturvedi

<p align="center">
<img src = "https://media-exp1.licdn.com/dms/image/C4E03AQHfb4nZEZKXhQ/profile-displayphoto-shrink_400_400/0/1615868393779?e=1638403200&v=beta&t=BU8HkWr2Bxq0OVXqaQcHSDHKnZ6l9n9ttL4O5oSHy2w"  height="120" alt="Nitish Chaturvedi">
</p>
<p align="center">
<a href = "https://github.com/waterupto"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/waterupto/">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>
</td>

</table>


