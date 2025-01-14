from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and tokenizer
model_dir = "../vit5-finetuned"  # Replace with your saved model path
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir).to(device)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_text = data.get('input')
        
        if not input_text:
            return jsonify({'error': 'Input text is required'}), 400

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
        answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        return jsonify({
            'answer': answer,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)