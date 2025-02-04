import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model and tokenizer
model_dir = "../model"  # Replace with your saved model path
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir).to(device)

def generate_response(input_text):
    """
    Generate a response from the model given the input text.

    Args:
        input_text (str): The input text/question for the chatbot.

    Returns:
        str: The generated response from the model.
    """
    # Tokenize input
    encoded_input = tokenizer(
        input_text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    ).to(device)

    # Generate response
    output_ids = model.generate(
        input_ids=encoded_input["input_ids"],
        attention_mask=encoded_input["attention_mask"],
        max_length=50,
        num_beams=4,
        length_penalty=1.0,
        early_stopping=True,
        no_repeat_ngram_size=2
    )

    # Decode response
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# Test examples
test_examples = [
    "Xin chào",
    "Điều 1 của Bộ luật Dân sự quy định gì?",
    "Trừ điểm giấy phép lái xe có nằm trong phạm vi nghị định không?",
    "Trường Đại học Kiến Trúc ở đâu?",
]

print("\nTesting multiple examples:")
for test_input in test_examples:
    output = generate_response(test_input)
    print(f"\nInput: {test_input}")
    print(f"Output: {output}")
