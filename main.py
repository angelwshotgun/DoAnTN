from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Đường dẫn đến mô hình đã fine-tuned
model_dir = "C:\Users\\\z\\Documents\vu\\\python\\\vit5-abstractive-qa\\checkpoint-60"

# Load tokenizer và mô hình
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

# Đưa model về GPU hoặc CPU (tùy máy của bạn)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def answer_question(context, question):
    input_text = f"question: {question} context: {context}"
    
    # Tokenize input
    inputs = tokenizer(input_text, return_tensors='pt', max_length=128, truncation=True, padding='max_length').to(device)
    
    print("Input IDs:", inputs['input_ids'])
    print("Attention Mask:", inputs['attention_mask'])
    
    # Generate câu trả lời
    outputs = model.generate(
        inputs['input_ids'], 
        max_length=50,  # Điều chỉnh lại độ dài tối đa
        num_beams=3,      # Sử dụng beam search đơn giản
        do_sample=True,  # Cho phép sampling
        top_k=50,  # Số lượng token hàng đầu để sampling
    )
    
    # Decode và trả về câu trả lời
    if len(outputs) > 0:
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    else:
        answer = "Không có câu trả lời được sinh ra."
    with open("./a.txt", "w", encoding="utf-8") as f:
        f.write(answer)
    return answer

# Ví dụ
context = "QUYẾT ĐỊNH Về việc quy định mức thu học phí năm học 2024-2025"
question = "Quyết định này nói về vấn đề gì?"

answer = answer_question(context, question)

with open("./ket_qua.txt", "w", encoding="utf-8") as f:
    f.write(f"Câu trả lời: {answer}\n")
