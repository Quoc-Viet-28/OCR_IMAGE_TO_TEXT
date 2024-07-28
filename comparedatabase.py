import csv
import json

def read_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        return list(reader), header

def compare_strings(input_part, db_text):
    return input_part.lower() in db_text.lower()

def save_to_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False

def get_matching_rows(input_parts, csv_file_path, json_file_path):
    if not input_parts:
        print("No input parts provided.")
        return []

    reader, header = read_csv_file(csv_file_path)
    text_column_index = header.index('TenThuoc')
    matching_rows = []

    for i, input_part in enumerate(input_parts):
        print(f"Processing input part: '{input_part}'")
        if i == 0:
            for row in reader:
                if compare_strings(input_part, row[text_column_index]):
                    matching_rows.append(row)
        else:
            new_matching_rows = []
            for row in matching_rows:
                if compare_strings(input_part, row[text_column_index]):
                    new_matching_rows.append(row)
            matching_rows = new_matching_rows

        print(f"Matching rows after '{input_part}': {len(matching_rows)} found")
        if not matching_rows:
            break  # Stop if no matches are found

    if matching_rows:
        save_to_json(matching_rows, json_file_path)
    else:
        print("No matching rows found.")

    return matching_rows

# Example usage:
csv_file_path = r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\Data_TenThuoc\uniqueNone.csv"
json_file_path = r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\fullDatabaseNone.json"
input_parts = ["Atorvastatin", "20mg", "tablets", "vd"]

matching_rows = get_matching_rows(input_parts, csv_file_path, json_file_path)
print("Final matching rows:", matching_rows)
