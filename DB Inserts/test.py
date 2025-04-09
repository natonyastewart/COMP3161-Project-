import pandas as pd

# List of CSV file paths
csv_files = [
    "students.csv",
    "lecturers.csv",
    "admins.csv",
    "courses.csv"
]

# Function to check for duplicates in all columns of a CSV file
def check_for_duplicates(file):
    df = pd.read_csv(file)
    duplicates = df[df.duplicated(keep=False)]  # Find all rows that are duplicates
    return duplicates

# Check for duplicates in all the CSV files
for file in csv_files:
    duplicates = check_for_duplicates(file)
    
    if not duplicates.empty:
        print(f"Found duplicates in {file}:")
        print(duplicates)
    else:
        print(f"No duplicates found in {file}.")
