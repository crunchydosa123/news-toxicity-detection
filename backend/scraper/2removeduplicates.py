import csv

# Input and output CSV file names
input_csv = 'gnews_links2.csv'
output_csv = 'links2_unique.csv'

# Use a set to track unique links
unique_links = set()

# Read the input CSV file
with open(input_csv, mode='r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    
    # Skip the header row
    header = next(reader)
    
    # Add the header row to the unique links
    unique_links.add(tuple(header))
    
    # Read each row and add to the set if it's not a duplicate and not 'Sign in'
    for row in reader:
        if row and row[0] != 'Sign in':  # Check if text is not 'Sign in'
            unique_links.add(tuple(row))

# Write the unique links to the output CSV file
with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header row
    writer.writerow(header)
    
    # Write the unique rows
    for row in unique_links:
        writer.writerow(row)

print(f"Duplicates removed and 'Sign in' entries filtered out. Unique links saved to '{output_csv}'.")
