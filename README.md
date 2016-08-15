# Nmap Through Email

Nmap through email is script develop to help security researcher. Commands to scan ip address can be send over the email and can recieve the result by email.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

Python Libraries and tools required

```
[1]Nmap
[2]Python Libraries:-
	mail, getpass, imaplib, os, subprocess, random, thread, MIMEText, 
	MIMEApplication, MIMEMultipart, SMTP, smtplib, sys
```

### Installing

Make sure to install the nmap on the system. If script unable to find the nmap, please paste it in same folder as nmap

Starting the Script

```
[1]Enter the emails address from which script recieve the emails
[2]Provide the password.
[3]Rest will be handel by script
```

Warning

```
Make sure the email account has access through smtp and imap
```

## Request for scan

While sending request for nmap scan make sure to follow the following format

### Email Format

To add switch option to nmap,make sure to follow the format. For example
```
Subject of email:-  nmap -sV -A

Warning: Do not add any input or out switch in subject
```

To add Ip or domain list to nmap scan, make sure to follow the format. For example
```
Body of email:-  ip={192.168.1.1,192.168.1.2} OR
				 ip={scanme.nmap.org,nmap.org}
```
### Receiving Result 

Result will be recieved in 3 files. 
```
-Input file (Contain the scan list of ips/domains)
-Output file (Contain the result of scan in text file)
-Outout file (Contain the result as XML format)
```
## Authors

* **Gurjant Singh** - *Security Researcher*

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details
