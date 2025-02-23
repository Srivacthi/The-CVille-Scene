from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from load_csv import load_items_from_csv
import os
from openai import OpenAI
from datetime import datetime
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
        place = request.form.get('place')
        numPeople = request.form.get('numPeople')
        indoorOutdoor = request.form.get('activity')
        budget = request.form.get('budget')
        date = request.form.get('dateTime')

        dt_object = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        dayOfWeek = dt_object.strftime("%A") 
        time = dt_object.strftime("%I:%M %p")

        description = ""

        if place != "I don't know":
            description += "Category: " + place + ", "

        if numPeople == 1:
            description += "1 person, "
        else:
            description += numPeople + " people, "

        if indoorOutdoor == "Either":
            description += "indoor or outdoor, "
        else:
            description += indoorOutdoor + ", "

        description += "budget: " + budget + ", on " + dayOfWeek + " at " + time

        #print(description)
        
        #put the selected option in an openAI prompt and get the result
        client = OpenAI()
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Can you find me places to go in Charlottesville, Virginia with the following preferences: " + description + ". Could I have the results in the form of a .csv file with the following column headers: ‘Name’, ‘Website’, ‘Description’, ‘Category’, and ‘Location’? And please make sure the ‘Description’ and ‘Location’ have no commas, and that the ‘Location’ is a complete address. And get rid of any unnecessary quotation marks please."
            }
        ]
        )

        #store the results that openai gave in a .csv file
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

# @app.route('/reviews')
# def reviews():
#     return render_template('reviews.html')

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
            #getting form data
            rating = request.form['rating']
            event_name = request.form['event_name']
            description = request.form['description']
            date = request.form['date']
            #saving review
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
