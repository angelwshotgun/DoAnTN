from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and tokenizer
model_path = "../phobert-qa2"
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)

# Define confidence threshold
CONFIDENCE_THRESHOLD = 0.6  # Adjust as needed

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        question = data.get('question')
        context = data.get('context')
        
        if not question or not context:
            return jsonify({'error': 'Question and context are required'}), 400

        # Tokenize input
        inputs = tokenizer(
            question,
            context[:512],
            return_tensors="pt",
            max_length=258,
            truncation="only_second",
            padding="max_length"
        )

        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)
            start_logits = outputs.start_logits
            end_logits = outputs.end_logits

        start_prob = torch.softmax(start_logits, dim=-1)
        end_prob = torch.softmax(end_logits, dim=-1)

        start_index = torch.argmax(start_logits)
        end_index = torch.argmax(end_logits)

        # Calculate confidence
        confidence = (start_prob[0][start_index] + end_prob[0][end_index]) / 2

        # Check confidence threshold
        if confidence < CONFIDENCE_THRESHOLD:
            return jsonify({
                'answer': 'Không thể trả lời câu hỏi này.',
                'status': 'unrelated'
            })

        # Get answer
        tokens = inputs['input_ids'][0][start_index:end_index + 1]
        answer = tokenizer.decode(tokens, skip_special_tokens=True)

        return jsonify({
            'answer': answer,
            'status': 'success',
            'confidence': confidence.item()
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
