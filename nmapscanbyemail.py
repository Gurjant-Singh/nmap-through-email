#!/usr/bin/env python

#Imports
import email, getpass, imaplib, os , subprocess, random, thread, sys, smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

#User Input
user = raw_input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")
detach_dir = '.'

#If something goes wrong.
def something_wrong(From):
	print '[!]Something Worng..'
	subject="Aler! Something Worng"
	message="Hi, \nThere is some problem with Script.\nMight be problem with format. Send 'nmap help' as subject in email for help.\nOtherwise, Please contact the admin for solution\nThanks"
	send_help(From,subject,message)

#How to use, Reply back
def send_help(From,subject,message):
	print '[*]Sending help back...'
	try:
		emaillist = From
		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] = user
		msg['Reply-to'] = From
		 
		msg.preamble = 'Multipart massage.\n'
		 
		part = MIMEText(message)
		msg.attach(part)
		 
		server = smtplib.SMTP("smtp.gmail.com:587")
		server.ehlo()
		server.starttls()
		server.login(user, pwd)
		server.sendmail(msg['From'], emaillist , msg.as_string())
	except:
		print "[!]Some problem with sending help"

#Deleting files 
def deletefile(filename,result_filename1,result_filename2):
	try:
		os.remove('./'+filename)
		os.remove('./'+result_filename1)
		os.remove('./'+result_filename2)
	except:
		print "[!]Problem with deleting files"

#Creating a file for nmap input
def wirte_tofile(iplist,subject,From):
	print '[*]Creating a file..'
	filename= 'input_'+str(random.randrange(1,1000000,3))+'.txt'
	with open(filename, 'w') as output:
		for item in iplist:
			output.write(item + '\n')		
	startscan(subject,From,filename)

#Checking email address for ip/domain list
def find_ipaddress(mail,subject,From):
	if 'ip={' in mail:
		print '[*]Checking for ip address'
		start_iplist=mail.index("ip={")+4
		raw_list=str(mail[start_iplist:len(mail)])
		end_iplist=0
		for i in raw_list:
			if i == '}':
				break
			else:
				end_iplist=end_iplist+1
		iplist=raw_list[0:end_iplist]
		iplist=iplist.split(',')
		print '[*]Ip list found'
		wirte_tofile(iplist,subject,From)
	else:
		print '[!]No list found'
		something_wrong(From)

#Sending scan result back
def send_result(subject,From,filename,result_filename1,result_filename2):
	print '[*]Sending result back...'
	try:
		emaillist = From
		msg = MIMEMultipart()
		msg['Subject'] = 'Result for nmap scan ' + subject
		msg['From'] = user
		msg['Reply-to'] = From
		 
		msg.preamble = 'Multipart massage.\n'
		 
		part = MIMEText("Hi, please find the attached file for results")
		msg.attach(part)
		 
		part = MIMEApplication(open(result_filename1,"rb").read())
		part.add_header('Content-Disposition', 'attachment', filename=result_filename1)
		msg.attach(part)

		part = MIMEApplication(open(result_filename2,"rb").read())
		part.add_header('Content-Disposition', 'attachment', filename=result_filename2)
		msg.attach(part)

		part = MIMEApplication(open(filename,"rb").read())
		part.add_header('Content-Disposition', 'attachment', filename=filename)
		msg.attach(part)
		 
		server = smtplib.SMTP("smtp.gmail.com:587")
		server.ehlo()
		server.starttls()
		server.login(user, pwd)
		 
		server.sendmail(msg['From'], emaillist , msg.as_string())
		print '[*]Sending Compelete..'
		print '[*]Deleting files..'
		deletefile(filename,result_filename1,result_filename2)
		print '[*]Checking New Emails..'
	except:
		print "[!]Some problem with sending result back"

#Starting nmap scan
def startscan(subject,From,filename):
	try:
		print '[*]Starting Namp Scan'
		result_filename1= 'result_xml_'+str(random.randrange(1,1000000,2))+'.xml'
		result_filename2= 'result_text_'+str(random.randrange(1,1000000,3))+'.txt'
		command=subject+' -iL '+'./'+str(filename)+' -oX '+result_filename1 +' -o '+result_filename2
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		send_result(subject,From,filename,result_filename1,result_filename2)
	except:
		print "hi"

#Check for new emails from email id.
def checkemails(m):
	print '[*]Checking for new emails'
	while True:
		m.select("Inbox")
		resp, items = m.search(None, '(UNSEEN)') 
		items = items[0].split() 

		if items != None:
			for emailid in items:
			    resp, data = m.fetch(emailid, "(RFC822)") 
			    email_body = data[0][1]
			    mail = email.message_from_string(email_body) 

			    print "["+mail["From"]+"] :" + mail["Subject"]
			    subject=mail["Subject"]
			    From=mail["From"]
			    raw_text=str(mail)
			    try:
				    if subject=='nmap help':
				    	subject="How to use Email-nmap"
				    	message="Hi, \nFollow the instruction to use Email-nmap\n[1]Add the nmap and switch you want to use in subject.Example:- nmap -sS -Vv (Don't add any input or output switch)\n[2]Add the ip list in message.Example:- ip={192.168.1.1,192.168.1.2} (follow the format)\nEnjoy."
				    	send_help(From,subject,message)
				    else:
				    	thread.start_new_thread ( find_ipaddress, (raw_text,subject,From) )
			    except:
					something_wrong(From)
		else:
			print ""


def main():
	try:

		m = imaplib.IMAP4_SSL("imap.gmail.com")
		m.login(user,pwd)

		print '[*]Login Succesful'

	except:
		print '[*]Unable to Login'

	checkemails(m)

main()

