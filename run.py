from app import create_app, db
from app.models import QuoteRequests, Employee, JobData

app = create_app()

@app.shell_context_processor
def make_shell_context():
	return { 
	'db' : db,
	'quote' : QuoteRequests,
	'employee' : Employee,
	'jobs' : JobData
	}