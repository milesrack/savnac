from flask import Blueprint, render_template, request, Flask, session, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from .other import removeTags
import requests
import datetime
import random

pages = Blueprint('pages',__name__)

@pages.route('/')
def home():
	image = f'study_{random.randint(0,4)}.png'
	return render_template('home.html', user=current_user, image=image)

@pages.route('/courses')
@login_required
def list_courses():
	if request.args.get('assignments'):
		dest = 'assignments'
	elif request.args.get('announcements'):
		dest = 'announcements'
	else:
		dest = 'assignments'
	url = f'https://{current_user.domain}/api/v1/courses/'
	params = {'access_token':current_user.api_token.strip(),'enrollment_state':'active','exclude_blueprint_courses':'true','per_page':'100'}
	r = requests.get(url,params=params)
	data = [(item['id'], item['name']) for item in r.json()]
	return render_template('courses.html', user=current_user, data=data, dest=dest)

@pages.route('/courses/<course_id>/assignments')
@login_required
def list_assignments(course_id):
	url = f'https://{current_user.domain}/api/v1/courses/{course_id}/assignments/'
	params = {'access_token':current_user.api_token,'order_by':'due_at','per_page':'100','include':['submission']}
	r = requests.get(url,params=params)
	data = [(item['id'], item['name'], datetime.datetime.strptime(item['due_at'],'%Y-%m-%dT%H:%M:%Sz').strftime('%m/%d/%Y %I:%M %p') if item['due_at'] else None, item['points_possible'], item['submission']['workflow_state'].title()) for item in r.json()]
	data.reverse()
	return render_template('assignments.html', user=current_user, data=data, course_id=course_id)

@pages.route('/courses/<course_id>/announcements')
@login_required
def list_announcements(course_id):
	url = f'https://{current_user.domain}/api/v1/announcements/'
	params = {'access_token':current_user.api_token,'context_codes[]':f'course_{str(course_id)}','per_page':'100'}
	r = requests.get(url,params=params)
	data = r.json()
	for item in data:
		if item['posted_at']:
			item['posted_at'] = datetime.datetime.strptime(item['posted_at'],'%Y-%m-%dT%H:%M:%Sz').strftime('%m/%d/%Y %I:%M %p')
	return render_template('announcements.html', user=current_user, data=data, course_id=course_id)

@pages.route('/courses/<course_id>/assignments/<assignment_id>')
@login_required
def assignment_details(course_id,assignment_id):
	url = f'https://{current_user.domain}/api/v1/courses/{course_id}/assignments/{assignment_id}'
	params = {'access_token':current_user.api_token,'order_by':'due_at','include':['submission']}
	r = requests.get(url,params=params)
	data = r.json()
	if data['due_at']:
		due_date = datetime.datetime.strptime(data['due_at'],'%Y-%m-%dT%H:%M:%Sz').strftime('%m/%d/%Y %I:%M %p')
	else:
		due_date = None
	if data['description']:
		data['description'] = removeTags(data['description'])
	return render_template('assignment_details.html', user=current_user, data=data, course_id=course_id, due_date=due_date)

@pages.route('/courses/<course_id>/announcements/<announcement_id>')
@login_required
def announcement_details(course_id, announcement_id):
	url = f'https://{current_user.domain}/api/v1/announcements/'
	params = {'access_token':current_user.api_token,'context_codes[]':f'course_{str(course_id)}','per_page':'100'}
	r = requests.get(url,params=params)
	for item in r.json():
		if item['id'] == int(announcement_id):
			data = item
			if data['message']:
				data['message'] = removeTags(data['message'])
			if data['posted_at']:
				data['posted_at'] = datetime.datetime.strptime(data['posted_at'],'%Y-%m-%dT%H:%M:%Sz').strftime('%m/%d/%Y %I:%M %p')
			return render_template('announcement_details.html', user=current_user, data=data, course_id=course_id)

@pages.route('/todo')
@login_required
def todo():
	url = f'https://{current_user.domain}/api/v1/users/self/missing_submissions/'
	params = {'access_token':current_user.api_token}
	r = requests.get(url,params=params)
	data = r.json()
	for item in data:
		if item['due_at']:
			item['due_at'] = datetime.datetime.strptime(item['due_at'],'%Y-%m-%dT%H:%M:%Sz').strftime('%m/%d/%Y %I:%M %p')
	return render_template('todo.html', user=current_user, data=data)

@pages.route('/feedback', methods=['GET','POST'])
def feedback():
	#session.pop('_flashes', None)
	if request.method == 'POST':
		first_name = request.form.get('fname')
		last_name = request.form.get('lname')
		email = request.form.get('email')
		feedback = request.form.get('feedback')
		if len(first_name) == 0:
			flash('First name cannot be empty.', category='feedback-error')
		elif len(last_name) == 0:
			flash('Last name cannot be empty.', category='feedback-error')
		elif len(email) == 0:
			flash('Email cannot be empty.', category='feedback-error')
		elif len(feedback) == 0:
			flash('Feedback cannot be empty.', category='feedback-error')
		else:
			flash('Your feedback has been submitted!', category='feedback-success')
			print(first_name, last_name, email, feedback)
			return redirect(url_for('pages.feedback'))
	return render_template('feedback.html', user=current_user)

@pages.route('/help')
def help():
	return render_template('help.html', user=current_user)
