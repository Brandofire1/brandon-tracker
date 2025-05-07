
import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect

import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
LOG_FILE = 'workout_log.csv'

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
gc = gspread.authorize(CREDS)
SHEET_ID = '1gH7_mkt04PkiZ-AyEprsrx5StcXekkg8tGMlYu3jU7M'
worksheet = gc.open_by_key(SHEET_ID).sheet1

# Ensure header row exists in Google Sheet
existing = worksheet.get_all_values()
if not existing or existing[0][0] != 'Date':
    header = [
        'Date', 'Training Type', 'RPE', 'PRs',
        'Sprint Speed (ft/s)', 'Sleep (hrs)',
        'Soreness (1-10)', 'Stool Type',
        'Digestion Notes', 'Caffeine (mg)',
        'Energy (1-10)'
    ]
    worksheet.insert_row(header, 1)

# Ensure CSV has headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Date', 'Training Type', 'RPE', 'PRs',
            'Sprint Speed (ft/s)', 'Sleep (hrs)',
            'Soreness (1-10)', 'Stool Type',
            'Digestion Notes', 'Caffeine (mg)',
            'Energy (1-10)'
        ])

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        row = [
            datetime.today().strftime('%Y-%m-%d'),
            request.form['training_type'],
            request.form['rpe'],
            request.form['prs'],
            request.form['sprint_speed'],
            request.form['sleep'],
            request.form['soreness'],
            request.form['stool'],
            request.form['digestion_notes'],
            request.form['caffeine'],
            request.form['energy']
        ]
        # Append to CSV
        with open(LOG_FILE, 'a', newline='') as f:
            csv.writer(f).writerow(row)
        # Append to Google Sheet with logging
        try:
            worksheet.append_row(row, value_input_option='USER_ENTERED')
            print("✅ Google Sheet append successful")
        except Exception as e:
            print("❌ Error appending to Google Sheet:", repr(e))
        return redirect('/')

    entries = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            reader = csv.reader(f)
            next(reader)
            entries = list(reader)[-10:][::-1]

    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
