import os
import json

# Đường dẫn đến file SQuAD dataset
dataset_path = "./data/xdfixed2.json"

# Đường dẫn thư mục đầu ra
output_dir = "output"

# Hàm tạo thư mục nếu chưa tồn tại
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Đọc dữ liệu từ file SQuAD
with open(dataset_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Thư mục chính
context_dir = os.path.join(output_dir, "context")
question_dir = os.path.join(output_dir, "question")
answers_dir = os.path.join(output_dir, "answers")
answers_text_dir = os.path.join(answers_dir, "text")
answers_start_dir = os.path.join(answers_dir, "answer_start")

# Tạo các thư mục cần thiết
ensure_dir(context_dir)
ensure_dir(question_dir)
ensure_dir(answers_text_dir)
ensure_dir(answers_start_dir)

# Duyệt qua dữ liệu và lưu vào các thư mục
for article in data["data"]:
    for paragraph in article["paragraphs"]:
        # Lưu context
        context_file = os.path.join(context_dir, f"{paragraph['qas'][0]['id']}.txt")
        with open(context_file, "w", encoding="utf-8") as f:
            f.write(paragraph["context"])

        # Lưu question và answers
        for qa in paragraph["qas"]:
            # Lưu question
            question_file = os.path.join(question_dir, f"{qa['id']}.txt")
            with open(question_file, "w", encoding="utf-8") as f:
                f.write(qa["question"])

            # Lưu answers
            for answer in qa["answers"]:
                answer_text_file = os.path.join(answers_text_dir, f"{qa['id']}.txt")
                with open(answer_text_file, "w", encoding="utf-8") as f:
                    f.write(answer["text"])

                answer_start_file = os.path.join(answers_start_dir, f"{qa['id']}.txt")
                with open(answer_start_file, "w", encoding="utf-8") as f:
                    f.write(str(answer["answer_start"]))

print("Dataset has been split and saved into folders!")
