from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from load_csv import load_items_from_csv
import os
from openai import OpenAI
import csv
import re

load_dotenv()

app = Flask(__name__)
app.config['OpenAI_API_KEY'] = os.getenv('OpenAI_API_KEY')

reviews_table = []

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    selected_option = None

    if request.method == 'POST':
        selected_option = request.form.get('dropdown_option')  

        if not selected_option:
            return render_template('home.html', selected_option=None)

        #put selected option in openAI prompt and get result
        client = OpenAI()
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Whare are some " +  selected_option + " in Charlottesville, VA? Can I have an itemized list in the form of a CSV file with column headers: 'Name', 'Website', 'Description', 'Category', and 'Location'? Make sure the Description and Location have no commas"
            }
        ]
        )

        openai_response = completion.choices[0].message.content
        match = re.search(r"```.*?\n(.*?)\n```", openai_response, re.DOTALL)
        csv_content = match.group(1) if match else openai_response 


        csv_filename = "results.csv"

        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)


            for line in csv_content.split("\n"):
                writer.writerow(line.split(","))

        return redirect(url_for('match_results'))

    return render_template('home.html', selected_option=selected_option)

@app.route('/matches')
def match_results():
    items = load_items_from_csv('results.csv')
    return render_template('match-results.html', items=items)


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    reviews_sorted = reviews_table
    sort_by = 'date'
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'sort':
            sort_by = request.form.get('sort_by', 'rating') 
            if sort_by == 'rating':
                reviews_sorted = sorted(reviews_table, key=lambda x: x['rating'], reverse=True)
            elif sort_by == 'date':
                reviews_sorted = sorted(reviews_table, key=lambda x: x['date'], reverse=True)
        elif action == 'submit_review':
            rating = request.form['rating']
            event_name = request.form['event_name']
            description = request.form['description']
            date = request.form['date']
            reviews_table.append({
                'rating': rating,
                'event_name': event_name,
                'description': description,
                'date': date
            })
            return redirect(url_for('reviews'))
    return render_template('reviews.html', reviews_table=reviews_sorted, sort_by=sort_by)

if __name__ == '__main__':
    app.run(debug=True)
