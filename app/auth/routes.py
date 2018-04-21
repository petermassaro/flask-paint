from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import EmployeeLoginForm
from app.models import Employee


@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.quoteRequests'))
	form = EmployeeLoginForm()
	if form.validate_on_submit():
		print("Form validated")
		employee = Employee.query.filter_by(email=form.email.data).first()
		print(employee, employee is None)
		if employee is None or not employee.check_password(form.password.data):
			flash('Invalid email or password')
			return redirect(url_for('main.quoteRequests'))
		login_user(employee, remember=form.remember_me.data)
		flash("Logged in as {}".format(employee.email))
		return redirect(url_for('main.quoteRequests'))
	return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('auth.login'))