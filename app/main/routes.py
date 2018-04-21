from app import db
from app.main import bp
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.main.forms import QuoteRequestForm, JobDataForm
from app.models import QuoteRequests, Employee, JobData
from app.sendSMS import sendSMS 
import datetime as dt 


@bp.route('/')
@bp.route('/index')
def index():
	return render_template('index.html')


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
	form = QuoteRequestForm()
	if form.validate_on_submit():
		quoteRequest = QuoteRequests(customer=form.customer.data, email=form.email.data,
			submit_time=dt.datetime.now(), street=form.street.data,
			city=form.city.data, state=form.state.data, zip_code=form.zip_code.data,
			phone=form.phone.data, time_requested=form.time.data, description=form.description.data)
		db.session.add(quoteRequest)
		db.session.commit()
		flash('Your quote request has been submitted')
		return redirect(url_for('main.index'))
	return render_template('quote.html', form=form)


@bp.route('/editQR/<quoteId>', methods=['GET', 'POST'])
@login_required
def edit(quoteId):
	quote = QuoteRequests.query.filter_by(id=quoteId).first()
	form = QuoteRequestForm(obj=quote)
	if form.validate_on_submit():
		quote.customer = form.customer.data
		quote.email = form.email.data
		quote.street = form.street.data
		quote.city = form.city.data
		quote.state = form.state.data
		quote.zip_code = form.zip_code.data
		quote.phone = form.phone.data
		print(form.email.data)
		db.session.commit()
		flash('Quote Request for {} has been edited'.format(quote.customer))
		return redirect(url_for('main.quoteRequests'))
	return render_template('quote.html', form=form)


@bp.route('/quoteRequests')
@login_required
def quoteRequests():
	page = request.args.get('page', 1, type=int)
	requests = QuoteRequests.query.order_by(QuoteRequests.submit_time.desc()).paginate(
		page, current_app.config['QRS_PER_PAGE'], False)
	next_url = url_for('main.quoteRequests', page=requests.next_num) \
		if requests.has_next else None
	prev_url = url_for('main.quoteRequests', page=requests.prev_num) \
		if requests.has_prev else None
	return render_template('quotes.html', quoteRequests=requests.items,
		next_url=next_url, prev_url=prev_url)


@bp.route('/jobentry', methods=['GET', 'POST'])
@login_required
def jobentry(quoteId=0):
	form = JobDataForm()
	if form.validate_on_submit():
		jobData = JobData(quote_id=quoteId, customer=form.customer.data, room_volume=form.room_volume.data,
			wall_area=form.wall_area.data, window_area=form.window_area.data, door_area=form.door_area.data,
			patchwork=form.patchwork.data, damages=form.damages.data, trim=form.trim.data,
			current_sheen=form.current_sheen.data, current_color=form.current_color.data,
			previous_paint=form.previous_paint.data, other=form.other.data)
		db.session.add(jobData)
		db.session.commit()
		flash("Job information submitted")
		return redirect(url_for("main.quoteRequests"))
	return render_template('jobentry.html', form=form)


@bp.route('/smsCustomerDetails/<messageContent>', methods=['GET','POST'])
@login_required
def textCustDetails(messageContent):
	sendSMS('6108126892', messageContent)
	return redirect(url_for('main.quoteRequests'))