#-*-coding:utf-8 -*-

import re
import poplib
import email        #
import email.header #
import os, sys
import time


host = ""
username = ""
password = ""
bossEmail = ""
timeLimit = ""

def configuration():
	'''
	effect: configure the basic information from the file MCC_config.ini.
	throw: when the file is not exit, throw an exception.
	'''
	global host, username, password, bossEmail, timeLimit
	try:
		fullPath = os.path.realpath(__file__)
		filePath = '%s/MCC_config.ini' % os.path.dirname(fullPath) 
		configFile = open(filePath)
	except IOError,e:
		print "The file is not exist" + e
		exit()

	information = configFile.readlines()
	host = search_word(r'host:(?: *)?(.*?)\n',information[0])
	username = search_word(r'username:(?: *)?(.*?com)\n',information[1])
	password = search_word(r'password:(?: *)?(.*?)\n',information[2])
	bossEmail = search_word(r'boss_email:(?: *)?(.*?com)\n',information[3])
	timeLimit = int(search_word(r'time_limit:(?: *)?([0-9]+)',information[4]))   # convert string to int
	configFile.close()

def search_word(w, s):
	'''
	require: w and s are both not empty
	w: regular expression, the part of word you want to return must be parenthesed
	s: string
	effect: return the part of word in w that matchs
	throw: when there is no w in s, throw an exception
	'''

	# This is a function in re, re.S tells the function to match all the character except /n.
	# And the group(), it determines which part to return.
	# For more details, you can go to https://docs.python.org/2/library/re.html
	matched = re.search(w, s, re.S).group(1)  
	if matched == None:
		raise "String does not contain the pattern", s
	return matched

def extract_mail_time(s):
	'''
	require: s is a string like this, 'Mon, 27 Apr 2015 08:30:49 +0800'
	effect: extract the day, month, year, hour, minute for the string
			return a list[year, month, day, hour, minute]
	'''
	months = ['dammy', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
			  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	year = int(search_word(r'.*, [0-9]+ [a-zA-Z]+ ([0-9]+) ', s))
	month = months.index(search_word(r'.*, [0-9]+ ([a-zA-Z]+) ', s))
	day = int(search_word(r', 0?([0-9]+) ', s))
	hour = int(search_word(r' 0?([0-9]+):', s))
	minute = int(search_word(r':0?([0-9]+):', s))
	return [year, month, day, hour, minute]

def is_leapyear(year):
	'''
	require: year must be a positive int number.
	effect: return true if year is leap, else false.
	'''
	if ((year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)):
		return True
	else:
		return False

def change_time_into_minutes(time):
	'''
	require: time is a list, and must be in the form of [year, month, day, hour, minute].
	effect: change the time into minutes regarding [1, 1, 1, 0, 0] as starting time.
	'''
	minutes400 = 97*366*24*60 + (400-97)*365*24*60  # The total minutes of 400 years(4 century and 
													# last year must be leap year).

	minutes100 = 24*366*24*60 + (100-24)*365*24*60  # The total minutes of 100 years(1 cencury and
													# last year must be common year).
	
	minutes4 = 366*24*60 + 3*365*24*60

	dayOfMonths = [31, 28, 31, 30, 31, 30,			# attention, it represents common year.
				   31, 31, 30, 31, 30, 31]          # So the second month only has 28 days.

	year = time[0] -1
	totalMinutesOf400 = year / 400 * minutes400
	totalMinutesOf100 = (year % 400) / 100 * minutes100
	totalMinutesOf4 = (year % 100) / 4 * minutes4
	restMinutesOf4 = (year % 4) * 365*24*60

	if is_leapyear(time[0]):
		dayOfMonths[1] = 29
	rest = sum(dayOfMonths[0: (time[1]-1)])*24*60 + (time[2]-1)*24*60 + time[3]*60 +time[4]
	total = totalMinutesOf400 + totalMinutesOf100 + totalMinutesOf4 + restMinutesOf4 + rest
	return total

def is_numbers_in_precision(firstNumber, secondNumber, precision):
	'''
	require: These three parameters are all numbers(int or float)
			 Precision must not be negative.
	effect: if (firstNumber - secondeNumber) <= precision, return True, else False.
	'''
	if abs(firstNumber - secondNumber) <= precision:
		return True
	else:
		return False

def login_email():
	'''
	effect: use poplib to login in the email and read the email messages.
			If the email is from boss email, deal with the command from the subject.
	notice: Here I use a 163 email, I haven't test other email providers.
	'''

	precision = 5 # Represents 5 minutes, to determine the email is new or not.

	# The functions below are from poplib.
	# For more information, go to https://docs.python.org/2/library/poplib.html
	emailServer = poplib.POP3(host)
	emailServer.user(username)
	emailServer.pass_(password)
	emailServer.set_debuglevel(1)
	emailServer.encoding = 'utf-8'
	emailMsgNum, emailSize = emailServer.stat()
	bossSents = False
	isNewEmail = False
	command = ''
	for piece in emailServer.retr(emailMsgNum)[1]: # Just check the lastest email.
		if bossEmail in piece:
			bossSents = True
		elif piece.startswith('Subject: '):
			command = piece[len('Subject: '):]
		elif piece.startswith('Date: '):
			emailSendedTime = extract_mail_time(piece[len('Data: '):])
			totalMinutesOfEmail = change_time_into_minutes(emailSendedTime)
			localTime = extract_mail_time(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
			totalMinutesOfLocal = change_time_into_minutes(localTime)
			if is_numbers_in_precision(totalMinutesOfEmail, totalMinutesOfLocal, precision):
				isNewEmail = True

	if bossSents and isNewEmail:
		deal_command(command)

def deal_command(c):
	'''
	effect: using cmd to executive the command
	require: c in commands
	c: command
	'''
	commands = {'shut': 'C:\Windows\System32\shutdown.exe -f -s -t 10 -c closing...'}
	if c in commands:
		os.system(commands[c])
	else:
		print "The subject of the email from boss has no meaning----", c

def setup():
	configuration()
	login_email()


if __name__ == '__main__':
	setup()
	while True:
		time.sleep(timeLimit)
		login_email()






