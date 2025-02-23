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
        selected_option = request.form.get('dropdown_option')  # Store selected value

        if not selected_option:
            return render_template('home.html', selected_option=None)

        #put the selected option in an openAI prompt and get the result
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

        #store the results that openai gave in a .csv file
        openai_response = completion.choices[0].message.content
        match = re.search(r"```.*?\n(.*?)\n```", openai_response, re.DOTALL)
        csv_content = match.group(1) if match else openai_response 


        # Define the filename
        csv_filename = "results.csv"

        # Write extracted content to CSV
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)


            # Split text into lines and write each as a row
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
    if request.method == 'POST':
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
    return render_template('reviews.html', reviews_table=reviews_table)

if __name__ == '__main__':
    app.run(debug=True)
