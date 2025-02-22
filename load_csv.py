import csv

def load_items_from_csv(filename):
    items = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                'name': row['Name'],
                'address': row['Address'],
                'cuisine': row['Type of Cuisine']
            }
            items.append(item)
    return items

# Example usage
filename = 'test_file.csv'
items = load_items_from_csv(filename)
print(items)
