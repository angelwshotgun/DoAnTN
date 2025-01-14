import csv
import json
from sklearn.utils import shuffle

# Đường dẫn tới file dữ liệu (thay bằng file thực tế của bạn)
input_file = "data.csv"
output_json_file = "formatted_data.json"

# Đọc dữ liệu từ file CSV
data = []
with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)  # Đọc file CSV có header
    for row in reader:
        intent = row["Intent"]  # Cột Intent
        example = row["Example"]  # Cột Example
        response = row["Response"]  # Cột Response
        data.append({"intent": intent, "example": example, "response": response})

# Tạo dữ liệu JSON theo cấu trúc yêu cầu
formatted_data = {"intents": []}
intent_dict = {}

# Gom nhóm theo intent
for item in data:
    intent = item["intent"]
    example = item["example"]
    response = item["response"]
    if intent not in intent_dict:
        intent_dict[intent] = {"intent": intent, "examples": [], "responses": []}
    intent_dict[intent]["examples"].append(example)
    intent_dict[intent]["responses"].append(response)

# Đưa dữ liệu vào danh sách intents
for intent_data in intent_dict.values():
    formatted_data["intents"].append(intent_data)

# Shuffle dữ liệu để tăng tính đa dạng
formatted_data["intents"] = shuffle(formatted_data["intents"], random_state=42)

# Ghi dữ liệu JSON ra file
with open(output_json_file, "w", encoding="utf-8") as f:
    json.dump(formatted_data, f, ensure_ascii=False, indent=4)

print(f"Formatted data saved to {output_json_file}")
