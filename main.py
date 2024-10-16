import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments, TrainerCallback
from datasets import Dataset
import torch

# Kiểm tra và in ra thiết bị (CPU hoặc GPU)
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

# Tạo dataframe để lưu trữ dữ liệu
df = pd.DataFrame({
    'context': context_data,
    'question': question_data,
    'answer': answer_data
}) 
print("Data loaded into dataframe.")

# Tải tokenizer và mô hình từ VietAI/vit5-large
model_name = "VietAI/vit5-large"
print(f"Loading model and tokenizer from: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.to(device)  # Đưa mô hình lên thiết bị (GPU hoặc CPU)
print("Model and tokenizer loaded.")

# Tokenize dữ liệu
def tokenize_text(context, question, answer, max_length=512):
    # T5 sử dụng format 'question: ... context: ...' cho đầu vào
    input_text = "question: " + question + " context: " + context
    target_text = answer
    return tokenizer(
        input_text,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    ), tokenizer(
        target_text,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )

# Tokenize các dòng trong dataframe
print("Tokenizing data...")
df['input_ids'], df['labels'] = zip(*df.apply(lambda x: tokenize_text(x['context'], x['question'], x['answer']), axis=1))
print("Data tokenized.")

# Xử lý dữ liệu đầu vào cho mô hình
def process_dataset(df):
    input_ids = []
    attention_mask = []
    labels = []
    
    for idx, row in df.iterrows():
        input_id = row['input_ids']['input_ids'].squeeze().tolist()
        mask = row['input_ids']['attention_mask'].squeeze().tolist()
        label = row['labels']['input_ids'].squeeze().tolist()
        input_ids.append(input_id)
        attention_mask.append(mask)
        labels.append(label)
        
    return {
        'input_ids': input_ids,
        'attention_mask': attention_mask,
        'labels': labels
    }

# Tạo dataset từ dataframe
print("Creating datasets for training and evaluation...")
train_df, eval_df = train_test_split(df, test_size=0.2, random_state=42)

train_dataset = Dataset.from_dict(process_dataset(train_df))
eval_dataset = Dataset.from_dict(process_dataset(eval_df))
print("Datasets created.")

# Callback để in ra tiến trình sau mỗi bước
class ProgressCallback(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % 100 == 0:  # In sau mỗi 100 steps
            print(f"Step: {state.global_step}, Loss: {state.loss}, Epoch: {state.epoch}")

# Thiết lập các thông số training (giảm batch size xuống 4)
training_args = TrainingArguments(
    output_dir="./vit5-abstractive-qa",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,  # Giảm batch size
    per_device_eval_batch_size=4,   # Giảm batch size
    eval_strategy="epoch",          # Đánh giá sau mỗi epoch
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=100,  # In log sau mỗi 100 steps
    report_to="none"  # Tắt việc gửi log lên dịch vụ bên ngoài
)
print("Training arguments set.")

# Khởi tạo Trainer cho T5 với callback để in tiến trình
print("Initializing Trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    callbacks=[ProgressCallback()]  # Thêm callback để in tiến trình
)
print("Trainer initialized.")

# Bắt đầu fine-tuning
print("Starting training...")
trainer.train()

# Lưu mô hình đã fine-tuned
print("Saving model and tokenizer...")
trainer.save_model("./vit5-abstractive-qa")
tokenizer.save_pretrained("./vit5-abstractive-qa")

print("Fine-tuning completed and model saved.")
