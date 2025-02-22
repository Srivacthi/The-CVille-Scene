from flask import Flask, render_template, request
from dotenv import load_dotenv
from load_csv import load_items_from_csv
import os
from openai import OpenAI
import csv
import re

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    selected_option = None

    if request.method == 'POST':
        selected_option = request.form.get('dropdown_option')  # Store selected value
        print(selected_option)

        #put the selected option in an openAI prompt and get the result
        client = OpenAI()
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Whare are some " +  selected_option + " in Charlottesville, VA? Can I have an itemized list in the form of a csv file that has 5 features: the name of the place, a link to the place's website, the location, and description, and category?"
            }
        ]
        )

        #store the results that openai gave in a .csv file
        openai_response = completion.choices[0].message.content
        match = re.search("```.*?\n(.*?)\n```", openai_response, re.DOTALL)
        csv_content = match.group(1)

        # Define the filename
        csv_filename = "results.csv"

        # Write extracted content to CSV
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)


            # Split text into lines and write each as a row
            for line in csv_content.split("\n"):
                writer.writerow(line.split(","))

        print(f"Selected option: {selected_option}")  # Debugging

    return render_template('match-results.html')
    #return render_template('home.html', selected_option=selected_option)

@app.route('/matches')
def match_results():
    items = load_items_from_csv('test_file.csv')
    return render_template('match-results.html', items=items)

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

if __name__ == '__main__':
    app.run(debug=True)
