from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import database

load_dotenv()

app = Flask(__name__)

with app.app_context():
    database.setup()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')
# Some are from https://www.geeksforgeeks.org/python/making-a-flask-app-using-a-postgresql-database/
@app.route('/submit', methods=['POST'])
def submit():
    text_input = request.form.get('text_input')
    radio_choice = request.form.get('radio_choice')
    select_choice = request.form.get('select_choice')
    # return True if it's on
    if request.form.get('checkbox') == 'on':
        checkbox = True
    else:
        checkbox = False
    # return empty string if not provided
    textarea_input = request.form.get('textarea_input', '')

    database.add_survey_response(text_input, radio_choice, select_choice, checkbox, textarea_input)
    return render_template('thanks.html')

@app.route('/decline')
def decline():
    return render_template('decline.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/api/results')
def api_results():
    if request.args.get('reverse') == 'true':
        reverse = True
    else:
        reverse = False
    results = database.get_survey_results(reverse)
    return jsonify(results)

@app.route('/admin/summary')
def admin_summary():
    results = database.get_survey_results(False)
    return render_template('summary.html', results=results)