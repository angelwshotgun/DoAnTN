import os
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, DataCollatorWithPadding, Trainer, TrainingArguments, TrainerCallback
from datasets import Dataset
import json

# Kiểm tra thiết bị (CPU hoặc GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Tải PhoBERT và tokenizer
model_name = "vinai/phobert-base-v2"
print(f"Loading model and tokenizer from: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
model.to(device)  # Đưa mô hình lên GPU hoặc CPU
print("Model and tokenizer loaded.")

# Đường dẫn đến file JSON chứa dữ liệu theo định dạng SQuAD
json_file_path = "C:\\Users\\z\\Documents\\vu\\python\\DoAnTN\\flask_squad_app\\data\\squad.json"

# Load dữ liệu từ file JSON
print(f"Loading dataset from: {json_file_path}")
with open(json_file_path, 'r', encoding='utf-8') as f:
    squad_data = json.load(f)

def split_context(context, max_tokens=256, overlap=50):
    """
    Chia context thành các đoạn nhỏ với độ dài tối đa và độ chồng lấn giữa các đoạn.
    
    Args:
        context (str): Đoạn văn cần chia.
        max_tokens (int): Số token tối đa cho mỗi đoạn.
        overlap (int): Số token chồng lấn giữa các đoạn liên tiếp.
    
    Returns:
        List[str]: Danh sách các đoạn văn nhỏ hơn.
    """
    # Tokenize toàn bộ context
    tokens = tokenizer.tokenize(context)
    total_tokens = len(tokens)
    
    # Chia đoạn văn
    chunks = []
    start = 0
    while start < total_tokens:
        end = min(start + max_tokens, total_tokens)
        chunk_tokens = tokens[start:end]
        chunks.append(tokenizer.convert_tokens_to_string(chunk_tokens))
        start += max_tokens - overlap  # Đảm bảo độ chồng lấn giữa các đoạn
    
    return chunks


# Khởi tạo danh sách để lưu dữ liệu huấn luyện đã xử lý
contexts = []
questions = []
answers = []

for item in squad_data["data"]:
    for paragraph in item["paragraphs"]:
        original_context = paragraph["context"]
        
        # Chia context thành các đoạn nhỏ
        context_chunks = split_context(original_context, max_tokens=256, overlap=50)
        
        for chunk_index, context_chunk in enumerate(context_chunks):
            for qa in paragraph["qas"]:
                question = qa["question"]
                answer_text = qa["answers"][0]["text"]
                
                # Đảm bảo answer_start là số nguyên
                answer_start = int(qa["answers"][0]["answer_start"])
                
                # Điều chỉnh answer_start cho từng chunk
                adjusted_start = answer_start - chunk_index * (256 - 50)
                
                # Bỏ qua nếu đáp án không nằm trong đoạn này
                if 0 <= adjusted_start < len(context_chunk):
                    contexts.append(context_chunk)
                    questions.append(question)
                    answers.append({"text": answer_text, "answer_start": adjusted_start})


print("Data extracted from JSON.")

# Tokenize dữ liệu và sử dụng answer_start có sẵn từ JSON
def process_row(context, question, answer):
    """
    Xử lý và tính toán vị trí token của đáp án với xử lý đặc biệt cho các token bị tách
    """
    # Tokenize toàn bộ input trước
    full_tokens = tokenizer(
        question,
        context,
        max_length=512,
        padding='max_length',
        truncation=True,
        return_tensors="pt"
    )
    
    # Convert về list và xóa chiều batch
    inputs = {k: v.squeeze(0).tolist() for k, v in full_tokens.items()}
    
    # Lấy tất cả các token
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'])
    
    # Tìm vị trí đáp án trong chuỗi token
    answer_text = answer["text"]
    
    # Tạo chuỗi từ các token để tìm kiếm
    text = ""
    start_position = -1
    end_position = -1
    
    # Duyệt qua các token để tìm vị trí bắt đầu và kết thúc của đáp án
    for i in range(len(tokens)):
        # Bỏ qua các token đặc biệt và padding
        if tokens[i] in ['<s>', '</s>', '<pad>']:
            continue
            
        # Xử lý token hiện tại
        current_token = tokens[i]
        if current_token.endswith('@@'):
            text += current_token[:-2]
        else:
            text += current_token + ' '
            
        # Tìm vị trí bắt đầu
        if start_position == -1 and answer_text in text:
            # Đi ngược lại để tìm token bắt đầu thực sự
            temp_text = ""
            for j in range(i, -1, -1):
                if tokens[j] in ['<s>', '</s>', '<pad>']:
                    continue
                if tokens[j].endswith('@@'):
                    temp_text = tokens[j][:-2] + temp_text
                else:
                    temp_text = tokens[j] + ' ' + temp_text
                if answer_text in temp_text:
                    start_position = j
                    break
        
        # Tìm vị trí kết thúc
        if start_position != -1 and end_position == -1:
            # Kiểm tra xem đã bao gồm toàn bộ đáp án chưa
            check_text = ""
            for j in range(start_position, i + 1):
                if tokens[j].endswith('@@'):
                    check_text += tokens[j][:-2]
                else:
                    check_text += tokens[j] + ' '
            if answer_text in check_text:
                end_position = i
                break
    
    # Nếu không tìm thấy, sử dụng vị trí mặc định
    if start_position == -1:
        start_position = 0
    if end_position == -1:
        end_position = len(tokens) - 1
        
    inputs['start_positions'] = start_position
    inputs['end_positions'] = end_position
    
    return inputs

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
    num_train_epochs=2,
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
