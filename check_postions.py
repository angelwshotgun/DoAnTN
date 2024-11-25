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
    """
    Xử lý và tính toán vị trí token của đáp án với xử lý đặc biệt cho các token bị tách
    """
    # Tokenize toàn bộ input trước
    full_tokens = tokenizer(
        question,
        context,
        max_length=258,
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
        end_position = start_position
        
    inputs['start_positions'] = start_position
    inputs['end_positions'] = end_position
    
    return inputs

def verify_token_positions(context, question, answer, tokenized_output, tokenizer):
    """
    Kiểm tra và hiển thị kết quả tokenization với xử lý cải tiến
    """
    # Decode các token
    tokens = tokenizer.convert_ids_to_tokens(tokenized_output['input_ids'])
    
    # Lấy vị trí start và end
    start_pos = tokenized_output['start_positions']
    end_pos = tokenized_output['end_positions']
    
    print("\n=== THÔNG TIN TOKENIZATION ===")
    print(f"\nCâu hỏi: {question}")
    print(f"Context: {context[:100]}...")
    print(f"Đáp án gốc: {answer['text']}")
    print(f"Vị trí ký tự trong context: {answer['answer_start']}")
    
    # In phân tích token
    print("\nPhân tích chuỗi token:")
    print("- Tokens câu hỏi:", tokenizer.tokenize(question))
    print("- Tokens đáp án:", tokenizer.tokenize(answer['text']))
    
    # In các token xung quanh answer
    print("\nCác token xung quanh đáp án:")
    start_idx = max(0, start_pos - 5)
    end_idx = min(len(tokens), end_pos + 6)
    
    # Tái tạo đáp án từ tokens đã chọn
    selected_answer = ""
    for i in range(start_pos, end_pos + 1):
        token = tokens[i]
        if token.endswith('@@'):
            selected_answer += token[:-2]
        else:
            selected_answer += token + ' '
    selected_answer = selected_answer.strip()
    
    # In token với màu để dễ nhận biết
    for i in range(start_idx, end_idx):
        if i == start_pos:
            print(f"\033[92m{i}: {tokens[i]} <== BẮT ĐẦU ĐÁP ÁN\033[0m")
        elif i == end_pos:
            print(f"\033[92m{i}: {tokens[i]} <== KẾT THÚC ĐÁP ÁN\033[0m")
        else:
            print(f"{i}: {tokens[i]}")
    
    print(f"\nĐáp án được tái tạo từ tokens: {selected_answer}")
    print(f"Đáp án gốc: {answer['text']}")
    
    # Kiểm tra độ chính xác
    accuracy = selected_answer.strip() == answer['text'].strip()
    print(f"Kết quả khớp: {'✓' if accuracy else '✗'}")
    
    return {
        'accuracy': 1 if accuracy else 0,
        'decoded_answer': selected_answer,
        'original_answer': answer['text'],
        'start_position': start_pos,
        'end_position': end_pos
    }

print("Đang xử lý dữ liệu...")
processed_data = [process_row(context, question, answer) 
                 for context, question, answer 
                 in zip(contexts, questions, answers)]

# Kiểm tra một số ví dụ
print("\nKiểm tra kết quả:")
for i in range(5):
    print(f"\n{'='*80}")
    print(f"VÍ DỤ {i+1}")
    verify_token_positions(
        contexts[i],
        questions[i],
        answers[i],
        processed_data[i],
        tokenizer
    )