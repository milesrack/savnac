import requests
import sys
import os
from os import name
from os import system
from colorama import *
from datetime import datetime
from bs4 import BeautifulSoup
import re
from time import sleep
import random
import yaml

# Clear screen
def clear():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')

# Function to remove html tags from data
def removeTags(text):
	TAG_RE = re.compile(r'<[^>]+>')
	return TAG_RE.sub('', text)

# Functions to color the text
##################################################
def red(text):
	red_text = Fore.RED + str(text) + Style.RESET_ALL
	return red_text

def yellow(text):
	yellow_text = Fore.YELLOW + str(text) + Style.RESET_ALL
	return yellow_text

def green(text):
	green_text = Fore.GREEN + str(text) + Style.RESET_ALL
	return green_text

def cyan(text):
	cyan_text = Fore.CYAN + str(text) + Style.RESET_ALL
	return cyan_text

def blue(text):
	blue_text = Fore.BLUE + str(text) + Style.RESET_ALL
	return blue_text

def magenta(text):
	magenta_text = Fore.MAGENTA + str(text) + Style.RESET_ALL
	return magenta_text
##################################################

# Function for error message
def invalid():
	print(red('Invalid selection!'))

# Function for connection errors
def connectionError():
	print(red('There was a connection error, please check your internet connection or your \'config.yml\' file for the correct configuration'))

# Gets the path of script; can be run from anywhere without new api token and domain file
def getPath():
	if name == 'nt':
		path = os.path.dirname(os.path.abspath(__file__)) + '\\'
	else:
		path = os.path.dirname(os.path.abspath(__file__)) + '/'
	return path

# Config stuff
def config():
	try:
		global api_token
		global domain
		path = getPath()
		config_file = path+'config.yml'
		try:
			with open(config_file) as config:
				doc = yaml.load(config, Loader=yaml.FullLoader)
				api_token = doc['api_token']
				domain = doc['domain']
		except (FileNotFoundError, TypeError, IOError):
			api_token = input('API token: ')
			domain = input('Enter your organization\'s domain (eg. browardschools.instructure.com): ')
		
		while api_token==None or len(api_token)!=69:
			clear()
			api_token = input('API token: ')
		while domain==None or len(domain)==0:
			clear()
			domain = input('Enter your organization\'s domain (eg. browardschools.instructure.com): ')

		config_dict = {'api_token':api_token, 'domain':domain}
		with open(config_file, 'w') as config:
			doc = yaml.dump(config_dict,config)
	except KeyboardInterrupt:
		clear()
		sys.exit()

# Lists currently enroled courses and returns a valid selection
def getCourses():
	clear()
	url = 'https://' + domain + '/api/v1/courses/'
	params = {'access_token':api_token,'enrollment_state':'active','per_page':'100'}
	try:
		r = requests.get(url,params)
	except OSError:
		connectionError()
		sys.exit()
	data = r.json()
	course_list = []
	for i in range(len(data)):
		course_id = data[i]['id']
		course_name = data[i]['name']
		course_list.append([course_id,course_name])
		menu_item = str('{:02d}'.format(i+1)) + ') ' + course_name
		print(green(menu_item))
	print(red('99) Exit'))
	while True:
		try:
			selection = int(input('Select a course: '))
			if selection == 99:
				clear()
				sys.exit()
			elif selection < 1 or selection > len(course_list):
				invalid()
				continue
			else:
				break
		except ValueError:
			invalid()
			continue
	return course_list[selection-1][0]

# Get announcements for a specific course
def getAnnouncements(course):
	clear()
	url = 'https://' + domain + '/api/v1/announcements/'
	course_code = 'course_' + str(course)
	params = {'access_token':api_token,'context_codes[]':course_code,'per_page':'100'}
	try:
		r = requests.get(url, params)
	except OSError:
		connectionError()
		sys.exit()
	data = r.json()
	announcement_list = []
	for i in range(len(data)):
		announcement_id = data[i]['id']
		announcement_title = data[i]['title']
		announcement_date = data[i]['posted_at']
		announcement_body = data[i]['message']
		announcement_list.append([announcement_id,announcement_title,announcement_date,announcement_body])
		menu_item = str('{:02d}'.format(i+1)) + ') ' + announcement_title
		print(magenta(menu_item))
	print(red('99) Back'))
	while True:
		try:
			selection = int(input('Select an announcement: '))
			if selection == 99:
				getAssignments(course)
			elif selection < 1 or selection > len(announcement_list):
				invalid()
				continue
			else:
				break
		except ValueError:
			invalid()
			continue
	_id = announcement_list[selection-1][0]
	title = announcement_list[selection-1][1]
	date = announcement_list[selection-1][2]
	description = announcement_list[selection-1][3]
	if description == None:
		description = 'None'
	else:
		description =  BeautifulSoup(description,'lxml')
		description = removeTags(str(description.body))
	if date == None:
		post_date = 'None'
	else:
		post_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
	announcement_url = 'https://' + domain + '/courses/' + str(course) + '/discussion_topics/' + str(_id)
	clear()
	print(magenta(title))
	print('Posted at:',green(post_date))
	print('URL:',cyan(announcement_url))
	print('Description:',description)
	input('\nPress ENTER to continue...')
	getAnnouncements(course)

# Lists assignments that are not yet due for the selected course
def getAssignments(course):
	clear()
	url = 'https://' + domain + '/api/v1/courses/' + str(course) + '/assignments/'
	params = {'access_token':api_token,'order_by':'due_at','bucket':'future','per_page':'100'}
	try:
		r = requests.get(url, params)
	except OSError:
		connectionError()
		sys.exit()
	data = r.json()
	assignment_list = []
	print(magenta('00) Announcements'))
	for i in range(len(data)):
		assignment_id = data[i]['id']
		assignment_due_date = data[i]['due_at']
		assignment_name = data[i]['name']
		assignment_description = data[i]['description']
		assignment_list.append([assignment_id,assignment_due_date,assignment_name,assignment_description])
		menu_item = str('{:02d}'.format(i+1)) + ') ' + assignment_name
		print(yellow(menu_item))
	print(red('99) Back'))
	while True:
		try:
			selection = int(input('Select an assignment: '))
			if selection == 0:
				getAnnouncements(course)
			elif selection == 99:
				main()
			elif selection < 1 or selection > len(assignment_list):
				invalid()
				continue
			else:
				break
		except ValueError:
			invalid()
			continue
	_id = assignment_list[selection-1][0]
	due = assignment_list[selection-1][1]
	title = assignment_list[selection-1][2]
	assignment_url = 'https://' + domain + '/courses/' + str(course) + '/assignments/' + str(_id)
	if due == None:
		due_date = 'None'
	else:
		due_date = datetime.strptime(due, "%Y-%m-%dT%H:%M:%SZ")
	description = assignment_list[selection-1][3]
	if description == None:
		description = 'None'
	else:
		description =  BeautifulSoup(description,'lxml')
		description = removeTags(str(description.body))
	clear()
	print(yellow(title))
	print('Due:',green(due_date))
	print('URL:',cyan(assignment_url))
	print('Description:',description)
	input('\nPress ENTER to continue...')
	getAssignments(course)

# Main function; continuous loop for fetching courses and assignments
def main():
	clear()
	config()
	while True:
		try:
			course = getCourses()
			getAssignments(course)
		except KeyboardInterrupt:
			clear()
			sys.exit()

# Call to main function
main()
