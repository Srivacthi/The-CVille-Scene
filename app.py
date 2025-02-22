from flask import Flask, render_template
from dotenv import load_dotenv
from load_csv import load_items_from_csv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/matches')
def match_results():
    items = load_items_from_csv('test_file.csv')
    return render_template('match-results.html', items=items)

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

if __name__ == '__main__':
    app.run(debug=True)