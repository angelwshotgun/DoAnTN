import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Load fine-tuned model and tokenizer
model_path = "C:\\Users\\z\\Documents\\vu\\python\\phobert-qa"  # Thư mục chứa mô hình đã tinh chỉnh
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForQuestionAnswering.from_pretrained(model_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def answer_question(context, question):
    # Encode inputs for PhoBERT
    inputs = tokenizer(question, context, return_tensors="pt", truncation=True).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract start and end scores
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    start_idx = torch.argmax(start_scores)
    end_idx = torch.argmax(end_scores) + 1

    # Decode the answer from the token IDs
    answer = tokenizer.decode(inputs["input_ids"][0][start_idx:end_idx], skip_special_tokens=True)
    return answer

# Example usage
context = "Thông tư 54/2022/TT-BKHĐT quy định về thủ tục cấp giấy chứng nhận đầu tư cho các dự án công nghệ cao. Thông tư yêu cầu các nhà đầu tư phải đáp ứng các tiêu chuẩn về công nghệ và bảo vệ môi trường để được cấp giấy chứng nhận."
question = "Thông tư 54/2022/TT-BKHĐT quy định về thủ tục gì?"
print(answer_question(context, question))
