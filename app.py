from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
def load_entries():
    if not os.path.exists('entries.json'):
        return []
    with open('entries.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_entries(entries):
    with open('entries.json', 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

entries = load_entries()

@app.route('/')
def index():
    return render_template('index.html', entries=entries)

@app.route('/entry/<int:entry_id>')
def detail(entry_id):
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry is None:
        return "Запись не найдена", 404
    return render_template('detail.html', entry=entry)

    @app.route('/add', methods=['GET', 'POST'])
def add():
    global entries
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_id = max([e['id'] for e in entries], default=0) + 1
        new_entry = {
            'id': new_id,
            'title': title,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        entries.append(new_entry)
        save_entries(entries)
        return redirect(url_for('index'))
    return render_template('add.html')

    @app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    global entries
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry is None:
        return "Запись не найдена", 404
    if request.method == 'POST':
        entry['title'] = request.form['title']
        entry['content'] = request.form['content']
        save_entries(entries)
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    global entries
    entries = [e for e in entries if e['id'] != entry_id]
    save_entries(entries)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    filtered = [e for e in entries if q in e['title'].lower()]
    return render_template('index.html', entries=filtered)

@app.route('/filter/week')
def filter_week():
    week_ago = datetime.now() - timedelta(days=7)
    filtered = []
    for e in entries:
        entry_date = datetime.strptime(e['date'], '%Y-%m-%d %H:%M:%S')
        if entry_date >= week_ago:
            filtered.append(e)
    return render_template('index.html', entries=filtered)

if __name__ == '__main__':
    app.run(debug=True)