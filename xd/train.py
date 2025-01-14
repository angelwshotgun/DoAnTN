import os
import json
import torch
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
)
from datasets import Dataset, concatenate_datasets

def load_data(json_path):
    """Load and process the JSON dataset."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    inputs = []
    outputs = []
    for intent_data in data["intents"]:
        examples = intent_data["examples"]
        responses = intent_data["responses"]

        for example in examples:
            response = responses[0]
            inputs.append(example)
            outputs.append(response)

    return inputs, outputs

# Kiểm tra thiết bị (CPU hoặc GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# **1. Load và xử lý dữ liệu**
json_path = "/content/datasets.json"  # Replace with your JSON file path
print(f"Loading data from: {json_path}")

inputs, outputs = load_data(json_path)

# Tách dữ liệu thành train và test
train_inputs, val_inputs, train_outputs, val_outputs = train_test_split(
    inputs, outputs, test_size=0.2, random_state=42
)

# Tạo datasets
train_dataset = Dataset.from_dict({"input_text": train_inputs, "output_text": train_outputs})
val_dataset = Dataset.from_dict({"input_text": val_inputs, "output_text": val_outputs})

# **2. Chọn mô hình và tokenizer**
model_name = "VietAI/vit5-base"
print(f"Loading model: {model_name}")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load model
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

# Tokenization
def preprocess_data(examples):
    # Tokenize inputs
    model_inputs = tokenizer(
        examples["input_text"],
        max_length=128,
        padding="max_length",
        truncation=True,
    )
    
    # Tokenize targets
    labels = tokenizer(
        text_target=examples["output_text"],
        max_length=128,
        padding="max_length",
        truncation=True,
    )
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Tokenize datasets
train_dataset = train_dataset.map(preprocess_data, batched=True)
val_dataset = val_dataset.map(preprocess_data, batched=True)

# Tăng cường dữ liệu (nếu cần)
train_dataset_doubled = concatenate_datasets([train_dataset, train_dataset])
val_dataset_doubled = concatenate_datasets([val_dataset, val_dataset])

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# **3. Huấn luyện mô hình**
training_args = TrainingArguments(
    output_dir="./vit5-finetuned",  # Thư mục lưu kết quả
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    logging_dir="./logs",
    logging_steps=20,
    report_to="none",
    fp16=torch.cuda.is_available(),  # Sử dụng mixed precision nếu có GPU
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset_doubled,
    eval_dataset=val_dataset_doubled,
    data_collator=data_collator,
    tokenizer=tokenizer,
)

# Bắt đầu huấn luyện
trainer.train()

# Đánh giá mô hình
metrics = trainer.evaluate()
print("Evaluation Metrics:", metrics)

# Lưu mô hình
model.save_pretrained("./vit5-finetuned")
tokenizer.save_pretrained("./vit5-finetuned")
