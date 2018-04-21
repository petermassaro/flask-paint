from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class QuoteRequests(db.Model):
	__tablename__ = 'quoterequests'
	id = db.Column(db.Integer, primary_key=True)
	customer = db.Column(db.String(120), index=True, unique=False)
	email = db.Column(db.String(120), index=True, unique=False)
	submit_time = db.Column(db.DateTime)
	street = db.Column(db.String(120), unique=False)
	city = db.Column(db.String(120), unique=False)
	state = db.Column(db.String(120), unique=False)
	zip_code = db.Column(db.Integer, unique=False)
	phone = db.Column(db.Integer, unique=False)
	time_requested = db.Column(db.String(120), unique=False)
	description = db.Column(db.String(240), unique=False)
	job = db.relationship('JobData', backref='data', lazy='dynamic')

	def __repr__(self):
		return '<QuoteRequest {}>'.format(self.customer)


class Employee(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	access_level = db.Column(db.String(120))
	phone = db.Column(db.String(20), unique=True)


	def __repr__(self):
		return '<User {}>'.format(self.email)

	def set_access_level(self, level):
		self.access_level = level

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class JobData(db.Model):
	__tablename__ = 'jobdata'
	id = db.Column(db.Integer, primary_key=True)
	quote_id = db.Column(db.Integer, db.ForeignKey('quoterequests.id'))
	customer = db.Column(db.String(120), index=True, unique=False)
	num_rooms = db.Column(db.Integer, unique=False)
	wall_area = db.Column(db.Integer, unique=False)
	num_windows = db.Column(db.Integer, unique=False)
	num_doors = db.Column(db.Integer, unique=False)
	patchwork = db.Column(db.String(120), unique=False)
	damages = db.Column(db.String(120), unique=False)
	trim = db.Column(db.String(120), unique=False)
	current_sheen = db.Column(db.String(120), unique=False)
	current_color = db.Column(db.String(120), unique=False)
	previous_paint = db.Column(db.String(120), unique=False)
	description = db.Column(db.String(500), unique=False)
	estimate = db.Column(db.Integer)

	def __repr__(self):
		return '<JobData {}>'.format(self.customer)



@login.user_loader
def load_user(id):
	return Employee.query.get(int(id))