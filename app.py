
from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = 'workout_log.csv'

# Ensure CSV has headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Date', 'Training Type', 'RPE', 'PRs', 'Sprint Speed (ft/s)',
            'Sleep (hrs)', 'Soreness (1-10)', 'Stool Type', 'Digestion Notes',
            'Caffeine (mg)', 'Energy (1-10)'
        ])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = [
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
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        return redirect('/')

    # Load recent entries
    entries = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            entries = list(reader)[-10:][::-1]  # last 10 entries, newest first

    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
