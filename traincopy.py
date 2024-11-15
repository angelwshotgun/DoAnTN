import os
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, DataCollatorWithPadding, Trainer, TrainingArguments, TrainerCallback
from datasets import Dataset
import json

# Kiểm tra thiết bị (CPU hoặc GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Đường dẫn đến file JSON chứa dữ liệu theo định dạng SQuAD
json_file_path = "C:\\Users\\z\\Documents\\vu\\python\\DoAnTN\\flask_squad_app\\data\\xdfixed2.json"

# Load dữ liệu từ file JSON
print(f"Loading dataset from: {json_file_path}")
with open(json_file_path, 'r', encoding='utf-8') as f:
    squad_data = json.load(f)

# Khởi tạo danh sách để lưu dữ liệu huấn luyện đã xử lý
contexts = []
questions = []
answers = []

# Duyệt qua dữ liệu JSON và trích xuất context, question, answer, và answer_start
for item in squad_data["data"]:
    for paragraph in item["paragraphs"]:
        context = paragraph["context"]
        for qa in paragraph["qas"]:
            question = qa["question"]
            answer_text = qa["answers"][0]["text"]
            answer_start = qa["answers"][0]["answer_start"]
            
            contexts.append(context)
            questions.append(question)
            answers.append({"text": answer_text, "answer_start": answer_start})

print("Data extracted from JSON.")

# Tải PhoBERT và tokenizer
model_name = "vinai/phobert-base-v2"
print(f"Loading model and tokenizer from: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
model.to(device)  # Đưa mô hình lên GPU hoặc CPU
print("Model and tokenizer loaded.")

# Tokenize dữ liệu và sử dụng answer_start có sẵn từ JSON
def process_row(context, question, answer):
    tokenizer.truncation_side = "left"
    inputs = tokenizer(
        question,
        context,
        max_length=258,
        padding='max_length',
        truncation=True
    )
    start_position = answer["answer_start"]
    end_position = start_position + len(answer["text"])
    
    return {
        'input_ids': inputs['input_ids'],
        'attention_mask': inputs['attention_mask'],
        'start_positions': start_position,
        'end_positions': end_position
    }

# Áp dụng tokenization cho toàn bộ dữ liệu
print("Processing data...")
processed_data = [process_row(context, question, answer) for context, question, answer in zip(contexts, questions, answers)]
print("Data processed.")

# Tạo dataset từ dữ liệu đã xử lý
train_df, eval_df = train_test_split(processed_data, test_size=0.2, random_state=42)
train_dataset = Dataset.from_dict({k: [d[k] for d in train_df] for k in train_df[0]})
eval_dataset = Dataset.from_dict({k: [d[k] for d in eval_df] for k in eval_df[0]})
print("Datasets created.")

data_collator = DataCollatorWithPadding(tokenizer, padding=True)

# Thiết lập các thông số training
training_args = TrainingArguments(
    output_dir="./phobert-qa",
    overwrite_output_dir=True,
    num_train_epochs=4,
    learning_rate=3e-5,
    weight_decay=0.01,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=2,
    eval_strategy="epoch",
    save_strategy = "epoch",
    logging_dir='./logs',
    logging_steps=50,
    report_to="none",
    fp16=True,
)
print("Training arguments set.")

# Khởi tạo Trainer cho PhoBERT với callback
print("Initializing Trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
)
print("Trainer initialized.")

# Bắt đầu fine-tuning
print("Starting training...")
trainer.train()

# Lưu mô hình đã fine-tuned
print("Saving model and tokenizer...")
trainer.save_model("./phobert-qa")
tokenizer.save_pretrained("./phobert-qa")

print("Fine-tuning completed and model saved.")
