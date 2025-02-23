import csv

def load_items_from_csv(filename):
    items = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                'name': row['Name'],
                'website' : row['Website'],
                'location': row['Location'],
                'description': row['Description'],
                'category': row['Category']
            }
            items.append(item)
    return items

# Example usage
filename = 'results.csv'
items = load_items_from_csv(filename)
print(items)
