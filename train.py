import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, DataCollatorWithPadding, Trainer, TrainingArguments, TrainerCallback
from datasets import Dataset
import torch

# Kiểm tra thiết bị (CPU hoặc GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Đặt đường dẫn đến thư mục datasets
dataset_dir = 'C:\\Users\\z\\Documents\\vu\\python\\DoAnTN\\datasets'
print("Loading dataset from:", dataset_dir)

# Đọc dữ liệu từ thư mục context
context_dir = os.path.join(dataset_dir, 'context')
context_files = [f for f in os.listdir(context_dir) if f.endswith('.txt')]
context_data = []
for file in context_files:
    with open(os.path.join(context_dir, file), 'r', encoding='utf-8') as f:
        context_data.append(f.read())
print("Loaded context data.")

# Đọc dữ liệu từ thư mục question
question_dir = os.path.join(dataset_dir, 'question')
question_files = [f for f in os.listdir(question_dir) if f.endswith('.txt')]
question_data = []
for file in question_files:
    with open(os.path.join(question_dir, file), 'r', encoding='utf-8') as f:
        question_data.append(f.read())
print("Loaded question data.")

# Đọc dữ liệu từ thư mục answer
answer_dir = os.path.join(dataset_dir, 'answer')
answer_files = [f for f in os.listdir(answer_dir) if f.endswith('.txt')]
answer_data = []
for file in answer_files:
    with open(os.path.join(answer_dir, file), 'r', encoding='utf-8') as f:
        answer_data.append(f.read())
print("Loaded answer data.")

# Tạo dataframe
df = pd.DataFrame({
    'context': context_data,
    'question': question_data,
    'answer': answer_data
})
print("Data loaded into dataframe.")

# Tải PhoBERT và tokenizer
model_name = "vinai/phobert-base-v2"
print(f"Loading model and tokenizer from: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
model.to(device)  # Đưa mô hình lên GPU hoặc CPU
print("Model and tokenizer loaded.")

# Hàm tự động tìm answer_start từ context
def find_answer_start(context, answer):
    # Tìm vị trí bắt đầu của câu trả lời trong context
    start_idx = context.find(answer)
    return start_idx if start_idx != -1 else None

# Tokenize dữ liệu và tính toán answer_start
def process_row(row):
    answer_start = find_answer_start(row['context'], row['answer'])
    if answer_start is not None:
        inputs = tokenizer(
            row['question'],
            row['context'],
            max_length=258,
            padding='max_length',
            truncation=True
        )
        return {
            'input_ids': inputs['input_ids'],
            'attention_mask': inputs['attention_mask'],
            'start_positions': answer_start,
            'end_positions': answer_start + len(row['answer'])
        }
    return None

# Xử lý dữ liệu và loại bỏ các hàng không có câu trả lời trong context
print("Processing data...")
processed_data = [process_row(row) for _, row in df.iterrows()]
processed_data = [d for d in processed_data if d is not None]
print("Data processed.")

# Tạo dataset từ dữ liệu đã xử lý
train_df, eval_df = train_test_split(processed_data, test_size=0.2, random_state=42)
train_dataset = Dataset.from_dict({k: [d[k] for d in train_df] for k in train_df[0]})
eval_dataset = Dataset.from_dict({k: [d[k] for d in eval_df] for k in eval_df[0]})
print("Datasets created.")

data_collator = DataCollatorWithPadding(tokenizer, padding=True)

# Callback để in tiến trình sau mỗi bước
class ProgressCallback(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % 100 == 0:  # In sau mỗi 100 steps
            print(f"Step: {state.global_step}, Loss: {state.loss}, Epoch: {state.epoch}")

# Thiết lập các thông số training
training_args = TrainingArguments(
    output_dir="./phobert-qa",
    overwrite_output_dir=True,
    num_train_epochs=30,
    learning_rate=5e-6,
    warmup_ratio=0.5,
    weight_decay=0.1,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    eval_strategy="epoch",
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=100,
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
    callbacks=[ProgressCallback()]
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
