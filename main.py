import pandas as pd
import numpy as np
import os

# Đặt đường dẫn đến thư mục datasets
dataset_dir = 'C:\\Users\\z\\Documents\\vu\\python\\DoAn\\datasets'

# Đọc dữ liệu từ thư mục context
context_dir = os.path.join(dataset_dir, 'context')
context_files = [f for f in os.listdir(context_dir) if f.endswith('.txt')]
context_data = []
for file in context_files:
    with open(os.path.join(context_dir, file), 'r', encoding='utf-8') as f:
        context_data.append(f.read())

# Đọc dữ liệu từ thư mục question
question_dir = os.path.join(dataset_dir, 'question')
question_files = [f for f in os.listdir(question_dir) if f.endswith('.txt')]
question_data = []
for file in question_files:
    with open(os.path.join(question_dir, file), 'r', encoding='utf-8') as f:
        question_data.append(f.read())

# Đọc dữ liệu từ thư mục answer
answer_dir = os.path.join(dataset_dir, 'answer')
answer_files = [f for f in os.listdir(answer_dir) if f.endswith('.txt')]
answer_data = []
for file in answer_files:
    with open(os.path.join(answer_dir, file), 'r', encoding='utf-8') as f:
        answer_data.append(f.read())

# Đọc dữ liệu từ thư mục label
label_dir = os.path.join(dataset_dir, 'label')
label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
label_data = []
for file in label_files:
    with open(os.path.join(label_dir, file), 'r', encoding='utf-8') as f:
        label_data.append(f.read())

# Tạo dataframe để lưu trữ dữ liệu
df = pd.DataFrame({
    'context': context_data,
    'question': question_data,
    'answer': answer_data,
    'label': label_data
}) 

from transformers import AutoTokenizer
import torch

# Tải tokenizer
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

# Hàm tokenize cho một chuỗi văn bản
def tokenize_text(text, max_length=512):
    return tokenizer(
        text,
        max_length=max_length,
        truncation=True,
        padding='max_length',
        return_tensors='pt'
    )

# Áp dụng tokenization cho từng cột
for column in ['context', 'question', 'answer']:
    # Tokenize
    tokenized = df[column].apply(lambda x: tokenize_text(x))
    
    # Tách các trường của tokenized output
    df[f'{column}_input_ids'] = tokenized.apply(lambda x: x['input_ids'].squeeze().tolist())
    df[f'{column}_attention_mask'] = tokenized.apply(lambda x: x['attention_mask'].squeeze().tolist())

# Xử lý cột label
df['label'] = df['label'].astype(int)

# Loại bỏ các cột văn bản gốc nếu cần
df = df.drop(columns=['context', 'question', 'answer'])

import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

dataset_dict = {
    'input_ids': df['context_input_ids'].tolist() + df['question_input_ids'].tolist() + df['answer_input_ids'].tolist(),
    'attention_mask': df['context_attention_mask'].tolist() + df['question_attention_mask'].tolist() + df['answer_attention_mask'].tolist(),
    'labels': df['label'].tolist() * 3  # Nhân 3 vì chúng ta ghép 3 cột
}

# Tạo Dataset
dataset = Dataset.from_dict(dataset_dict)

# Tải mô hình và tokenizer
model_name = "vinai/phobert-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)

# Chuẩn bị data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

# Cấu hình training arguments
training_args = TrainingArguments(
    output_dir="./phobert-fine-tuned",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_steps=10_000,
    save_total_limit=2,
    prediction_loss_only=True,
)

# Khởi tạo Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator,
)

# Bắt đầu fine-tuning
trainer.train()

# Lưu mô hình đã fine-tuned
trainer.save_model("./phobert-fine-tuned")

# Lưu tokenizer
tokenizer.save_pretrained("./phobert-fine-tuned")

print("Fine-tuning completed and model saved.")