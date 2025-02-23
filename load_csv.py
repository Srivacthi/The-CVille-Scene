import csv

def load_items_from_csv(filename):
    items = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            items.append({
                'name': row.get('Name', 'N/A'), 
                'website': row.get('Website', 'N/A'),
                'description': row.get('Description', 'N/A'),
                'category': row.get('Category', 'N/A'),
                'location': row.get('Location', 'N/A')
            })
        return items

# Example usage
filename = 'results.csv'
items = load_items_from_csv(filename)
print(items)
